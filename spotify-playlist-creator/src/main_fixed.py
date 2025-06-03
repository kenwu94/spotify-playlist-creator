import os
import sys
import time
from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
from dotenv import load_dotenv
import requests
import urllib.parse
import secrets
import logging
from datetime import datetime

# Add the src directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.playlist_routes import playlist_bp
from routes.auth_routes import auth_bp
from templates.html_template import HTML_TEMPLATE
from templates.login_template import LOGIN_TEMPLATE
from services.spotify_service import SpotifyService
from services.rate_limiter import rate_limit

# Load environment variables
load_dotenv()

# Configure basic logging for production
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='resources', static_url_path='/static')

# Use environment variables for production
app.secret_key = os.getenv('SECRET_KEY', os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here'))

# Configure session for production
app.config['SESSION_COOKIE_SECURE'] = True  # Use HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Spotify OAuth settings - Updated for production
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Dynamic redirect URI - use environment variable if set, otherwise default to localhost
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:5000/callback')

SPOTIFY_SCOPES = 'playlist-modify-public playlist-modify-private user-read-private user-read-email user-top-read user-read-recently-played user-library-read user-follow-read'

# Initialize Spotify service
spotify_service = SpotifyService()

# Register blueprints
app.register_blueprint(playlist_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

def require_auth():
    """Check if user is authenticated and refresh token if needed"""
    access_token = session.get('spotify_token')
    user_info = session.get('user_info')
    token_expires = session.get('spotify_token_expires', 0)
    
    if not access_token or not user_info:
        return False
    
    # Check if token is expired or expires within 5 minutes
    if token_expires < (int(time.time()) + 300):
        logging.info("🔄 Token expired or expiring soon, attempting refresh...")
        if refresh_user_token():
            logging.info("✅ Token refreshed successfully")
            return True
        else:
            logging.warning("❌ Token refresh failed")
            return False
    
    return True

def refresh_user_token():
    """Refresh the user's access token using the refresh token"""
    refresh_token = session.get('spotify_refresh_token')
    
    if not refresh_token:
        logging.error("❌ No refresh token available")
        return False
    
    try:
        token_url = 'https://accounts.spotify.com/api/token'
        token_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }
        
        response = requests.post(token_url, data=token_data)
        
        if response.status_code == 200:
            token_info = response.json()
            
            # Update session with new token
            session['spotify_token'] = token_info['access_token']
            session['spotify_token_expires'] = int(time.time()) + token_info.get('expires_in', 3600)
            
            # Refresh token might be rotated
            if 'refresh_token' in token_info:
                session['spotify_refresh_token'] = token_info['refresh_token']
            
            logging.info("✅ Token refreshed successfully")
            return True
        else:
            logging.error(f"❌ Token refresh failed: {response.status_code}")
            return False
            
    except Exception as e:
        logging.error(f"❌ Error refreshing token: {str(e)}")
        return False

@app.route('/')
def index():
    """Main page - shows the playlist creator"""
    logging.info("📄 Serving main page")
    return render_template_string(HTML_TEMPLATE)

@app.route('/login')
@rate_limit(max_requests=10, window_seconds=60, per='ip')
def login_page():
    """Display login page - separate from the main page"""
    # If user is already authenticated, redirect to main page
    if require_auth():
        logging.info("✅ User already authenticated, redirecting to main page")
        return redirect(url_for('index'))
    
    logging.info("📄 Serving login page")
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/callback')
@rate_limit(max_requests=5, window_seconds=60, per='ip')
def spotify_callback():
    """Handle Spotify OAuth callback"""
    logging.info("🔗 Processing Spotify OAuth callback")
    logging.info(f"🔗 Using redirect URI in callback: {SPOTIFY_REDIRECT_URI}")
    
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    logging.info(f"📥 Callback params - code: {'Present' if code else 'Missing'}, state: {'Present' if state else 'Missing'}, error: {error}")
    
    if error:
        logging.error(f"❌ Spotify authorization error: {error}")
        return redirect(url_for('login_page'))
    
    if not code:
        logging.error("❌ No authorization code received")
        return redirect(url_for('login_page'))
    
    # Verify state parameter
    session_state = session.get('oauth_state')
    logging.info(f"🔐 State verification - session: {'Present' if session_state else 'Missing'}, received: {'Present' if state else 'Missing'}")
    if not session_state or state != session_state:
        logging.error("❌ Invalid state parameter")
        return redirect(url_for('login_page'))
    
    try:
        # Exchange code for token
        token_url = 'https://accounts.spotify.com/api/token'
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }
        
        token_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        logging.info(f"🔍 Token exchange request with redirect_uri: {SPOTIFY_REDIRECT_URI}")
        
        response = requests.post(token_url, data=token_data, headers=token_headers)
        
        logging.info(f"🔍 Token exchange - Status: {response.status_code}")
        
        if response.status_code == 200:
            token_info = response.json()
            
            logging.info(f"✅ Token exchange successful")
            logging.info(f"🔍 Token scopes: {token_info.get('scope', 'No scopes returned')}")
            logging.info(f"🔍 Token type: {token_info.get('token_type', 'Unknown')}")
            logging.info(f"🔍 Token expires in: {token_info.get('expires_in', 'Unknown')} seconds")
            
            # Make session permanent for better persistence
            session.permanent = True
            
            # Store tokens in session
            session['spotify_token'] = token_info['access_token']
            session['spotify_refresh_token'] = token_info.get('refresh_token')
            session['spotify_token_expires'] = int(time.time()) + token_info.get('expires_in', 3600)
            
            # Get user info
            user_info = get_user_info(token_info['access_token'])
            if user_info:
                session['user_info'] = user_info
                session.pop('oauth_state', None)
                
                logging.info(f"✅ User authenticated: {user_info.get('display_name')}")
                return redirect(url_for('index'))
            else:
                logging.error("❌ Failed to get user info - redirecting to login")
                session.pop('oauth_state', None)
                return redirect(url_for('login_page'))
        else:
            logging.error(f"❌ Token exchange failed: {response.status_code}")
            logging.error(f"🔍 Response: {response.text}")
            return redirect(url_for('login_page'))
    
    except Exception as e:
        logging.error(f"❌ OAuth callback error: {str(e)}")
        return redirect(url_for('login_page'))

def get_user_info(access_token):
    """Get user information from Spotify"""
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Log token details for debugging (first/last 10 chars only for security)
        token_preview = f"{access_token[:10]}...{access_token[-10:]}" if len(access_token) > 20 else "short_token"
        logging.info(f"🔍 Making user info request with token: {token_preview}")
        
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        
        logging.info(f"🔍 User info request - Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            logging.info(f"✅ Successfully got user info for: {user_data.get('display_name', 'Unknown')}")
            return user_data
        elif response.status_code == 401:
            logging.error(f"❌ Failed to get user info: 401 - Token expired or invalid")
            logging.error(f"🔍 Response headers: {dict(response.headers)}")
            logging.error(f"🔍 Response: {response.text}")
            return None
        elif response.status_code == 403:
            logging.error(f"❌ Failed to get user info: 403 - Insufficient permissions or app configuration issue")
            logging.error(f"🔍 This usually means:")
            logging.error(f"   1. Redirect URI not configured in Spotify Dashboard")
            logging.error(f"   2. App needs additional scopes or approval")
            logging.error(f"   3. App is not in development mode")
            logging.error(f"🔍 Response headers: {dict(response.headers)}")
            logging.error(f"🔍 Response: {response.text}")
            
            # Test if the token works with other endpoints
            logging.info("🔍 Testing token with other Spotify endpoints...")
            
            # Test search endpoint (no special permissions needed)
            try:
                search_response = requests.get('https://api.spotify.com/v1/search?q=test&type=track&limit=1', headers=headers)
                logging.info(f"🔍 Search endpoint test: {search_response.status_code}")
                if search_response.status_code == 200:
                    logging.info("✅ Token works for search - issue is specifically with /me endpoint")
                else:
                    logging.error(f"❌ Search endpoint also failed: {search_response.text}")
            except Exception as e:
                logging.error(f"❌ Error testing search endpoint: {str(e)}")
            
            # Test playlists endpoint (requires playlist scopes)
            try:
                playlists_response = requests.get('https://api.spotify.com/v1/me/playlists?limit=1', headers=headers)
                logging.info(f"🔍 Playlists endpoint test: {playlists_response.status_code}")
                if playlists_response.status_code == 200:
                    logging.info("✅ Token works for playlists - issue is with user-read-private scope")
                elif playlists_response.status_code == 403:
                    logging.error("❌ Playlists endpoint also returns 403 - broader scope issue")
                else:
                    logging.error(f"❌ Playlists endpoint failed: {playlists_response.text}")
            except Exception as e:
                logging.error(f"❌ Error testing playlists endpoint: {str(e)}")
            
            return None
        else:
            logging.error(f"❌ Failed to get user info: {response.status_code}")
            logging.error(f"🔍 Response headers: {dict(response.headers)}")
            logging.error(f"🔍 Response: {response.text}")
            return None
    except Exception as e:
        logging.error(f"❌ Error getting user info: {str(e)}")
        return None

@app.route('/api/user')
def api_user():
    """Get current user info for the frontend"""
    if not require_auth():
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_info = session.get('user_info', {})
    return jsonify({
        'authenticated': True,
        'user': {
            'name': user_info.get('display_name', 'Unknown'),
            'email': user_info.get('email', ''),
            'id': user_info.get('id', ''),
            'image': user_info.get('images', [{}])[0].get('url', '') if user_info.get('images') else ''
        }
    })

@app.route('/health')
def health():
    """Health check endpoint for Vercel"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'redirect_uri': SPOTIFY_REDIRECT_URI
    }), 200

@app.route('/debug-auth')
def debug_auth():
    """Debug endpoint to check authentication configuration"""
    return jsonify({
        'client_id': SPOTIFY_CLIENT_ID[:10] + '...' if SPOTIFY_CLIENT_ID else 'Missing',
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'scopes': SPOTIFY_SCOPES,
        'session_info': {
            'has_token': bool(session.get('spotify_token')),
            'has_refresh_token': bool(session.get('spotify_refresh_token')),
            'has_user_info': bool(session.get('user_info')),
            'token_expires': session.get('spotify_token_expires', 0)
        }
    })

@app.route('/debug-spotify-token')
def debug_spotify_token():
    """Debug endpoint to test current Spotify token with various endpoints"""
    access_token = session.get('spotify_token')
    if not access_token:
        return jsonify({'error': 'No token in session'}), 401
    
    headers = {'Authorization': f'Bearer {access_token}'}
    results = {}
    
    # Test different endpoints
    endpoints = [
        ('search', 'https://api.spotify.com/v1/search?q=test&type=track&limit=1'),
        ('me', 'https://api.spotify.com/v1/me'),
        ('playlists', 'https://api.spotify.com/v1/me/playlists?limit=1'),
        ('player', 'https://api.spotify.com/v1/me/player')
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, headers=headers)
            results[name] = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'response': response.text[:500] if response.text else 'No response body'
            }
        except Exception as e:
            results[name] = {'error': str(e)}
    
    return jsonify({
        'token_preview': f"{access_token[:10]}...{access_token[-10:]}" if len(access_token) > 20 else "short_token",
        'token_expires': session.get('spotify_token_expires', 0),
        'current_time': int(time.time()),
        'endpoints': results
    })

@app.errorhandler(429)
def rate_limit_exceeded(error):
    logging.warning("🚦 Rate limit exceeded")
    return jsonify({'error': 'Rate limit exceeded'}), 429

# For local development
if __name__ == '__main__':
    print("🎵 Starting Spotify Playlist Creator...")
    print(f"🔗 Redirect URI: {SPOTIFY_REDIRECT_URI}")
    print("📍 Available routes:")
    print("   - Main page: http://127.0.0.1:5000/")
    print("   - Login page: http://127.0.0.1:5000/login")
    app.run(host='127.0.0.1', port=5000, debug=True)
