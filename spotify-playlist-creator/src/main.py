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
from templates.privacy_policy import PRIVACY_POLICY_TEMPLATE
from templates.terms_of_service import TERMS_OF_SERVICE_TEMPLATE
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
# Only use secure cookies in production (HTTPS)
is_production = os.getenv('ENVIRONMENT') == 'production' or os.getenv('VERCEL') == '1'
logging.info(f"🔍 Production mode: {is_production}")
logging.info(f"🔍 Environment: {os.getenv('ENVIRONMENT')}")
logging.info(f"🔍 Vercel: {os.getenv('VERCEL')}")

app.config['SESSION_COOKIE_SECURE'] = is_production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
app.config['SESSION_COOKIE_DOMAIN'] = None  # Allow subdomains

# Additional session configuration for Vercel
if is_production:
    app.config['SESSION_COOKIE_NAME'] = 'dreamify_session'
    app.config['SESSION_COOKIE_PATH'] = '/'

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
    
    logging.info(f"🔍 require_auth() - token: {'Present' if access_token else 'Missing'}, user_info: {'Present' if user_info else 'Missing'}")
    
    if not access_token:
        logging.warning(f"❌ Missing access token")
        return False
    
    # Check if token is expired or expires within 5 minutes
    current_time = int(time.time())
    if token_expires < (current_time + 300):
        logging.info(f"🔄 Token expired or expiring soon (expires: {token_expires}, current: {current_time}), attempting refresh...")
        if refresh_user_token():
            logging.info("✅ Token refreshed successfully")
            # Update token for user info check
            access_token = session.get('spotify_token')
        else:
            logging.warning("❌ Token refresh failed")
            return False
    
    # If we have a valid token but missing user_info, try to get it
    if not user_info and access_token:
        logging.info("🔄 Valid token but missing user_info, attempting to retrieve...")
        user_info = get_user_info(access_token)
        if user_info:
            session['user_info'] = user_info
            session.modified = True
            logging.info("✅ Successfully retrieved and stored user_info")
        else:
            logging.warning("⚠️ Could not retrieve user_info, but token is valid - allowing access")
            # Create minimal user info to prevent future failures
            session['user_info'] = {
                'id': 'unknown',
                'display_name': 'Spotify User',
                'email': None
            }
            session.modified = True
    
    logging.info("✅ Authentication check passed")
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
    
    try:        # Exchange code for token
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
        
        response = requests.post(token_url, data=token_data, headers=token_headers)
        
        logging.info(f"🔍 Token exchange - Status: {response.status_code}")
        
        if response.status_code == 200:
            token_info = response.json()
            
            logging.info(f"✅ Token exchange successful")
            logging.info(f"🔍 Token scopes: {token_info.get('scope', 'No scopes returned')}")
              # Make session permanent for better persistence
            session.permanent = True
            
            # Store tokens in session
            session['spotify_token'] = token_info['access_token']
            session['spotify_refresh_token'] = token_info.get('refresh_token')
            session['spotify_token_expires'] = int(time.time()) + token_info.get('expires_in', 3600)            # Get user info with retry mechanism - MORE AGGRESSIVE RETRY
            user_info = get_user_info(token_info['access_token'])
            logging.info(f"🔍 get_user_info returned: {user_info is not None}")
            
            # If first attempt fails, try up to 3 more times with increasing delays
            retry_count = 0
            while not user_info and retry_count < 3:
                retry_count += 1
                logging.warning(f"⚠️ User info attempt {retry_count} failed, retrying in {retry_count} seconds...")
                time.sleep(retry_count)  # 1s, 2s, 3s delays
                user_info = get_user_info(token_info['access_token'])
                logging.info(f"🔍 get_user_info retry {retry_count} returned: {user_info is not None}")
            
            # Clean up OAuth state regardless of user info success
            session.pop('oauth_state', None)
            
            if user_info and user_info.get('id') != 'unknown':
                session['user_info'] = user_info
                logging.info(f"✅ User authenticated: {user_info.get('display_name')}")
                logging.info(f"✅ Real user info stored in session")
            else:
                logging.error("❌ Failed to get real user info after all retries")
                
                # Try one more time with a fresh request to be absolutely sure
                logging.warning("🔄 Making final attempt to get user info...")
                final_user_info = get_user_info(token_info['access_token'])
                
                if final_user_info and final_user_info.get('id') != 'unknown':
                    session['user_info'] = final_user_info
                    logging.info(f"✅ Final attempt successful: {final_user_info.get('display_name')}")
                else:
                    # Only use minimal info as absolute last resort
                    logging.error("❌ All attempts to get real user info failed - using minimal fallback")
                    session['user_info'] = {
                        'id': 'unknown',
                        'display_name': 'Spotify User',
                        'email': None
                    }
                    logging.info("⚠️ Using minimal user info as last resort")
            
            # Force session commit
            session.modified = True
            
            logging.info(f"🔍 Final session keys: {list(session.keys())}")
            logging.info(f"🔍 Session token stored: {'spotify_token' in session}")
            logging.info(f"🔍 Session user_info stored: {'user_info' in session}")
            
            # Add ?from=login parameter to trigger proper post-login handling
            return redirect(url_for('index') + '?from=login')
        else:
            logging.error(f"❌ Token exchange failed: {response.status_code}")
            return redirect(url_for('login_page'))
    
    except Exception as e:
        logging.error(f"❌ OAuth callback error: {str(e)}")
        return redirect(url_for('login_page'))

def get_user_info(access_token):
    """Get user information from Spotify"""
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        logging.info(f"🔍 Making request to Spotify API with token: {access_token[:20]}...")
        
        response = requests.get('https://api.spotify.com/v1/me', headers=headers, timeout=10)
        
        logging.info(f"🔍 User info request - Status: {response.status_code}")
        logging.info(f"🔍 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            user_data = response.json()
            logging.info(f"✅ Successfully got user info for: {user_data.get('display_name', 'Unknown')}")
            logging.info(f"🔍 User data keys: {list(user_data.keys())}")
            return user_data
        elif response.status_code == 401:
            logging.error(f"❌ Failed to get user info: 401 - Token expired or invalid")
            logging.error(f"🔍 Response: {response.text}")
            return None
        elif response.status_code == 403:
            logging.error(f"❌ Failed to get user info: 403 - Insufficient permissions")
            logging.error(f"🔍 Response: {response.text}")
            return None
        else:
            logging.error(f"❌ Failed to get user info: {response.status_code}")
            logging.error(f"🔍 Response: {response.text}")
            return None
    except requests.exceptions.Timeout:
        logging.error(f"❌ Timeout error getting user info")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Request error getting user info: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"❌ Unexpected error getting user info: {str(e)}")
        return None

@app.route('/api/user')
def api_user():
    """Get current user info for the frontend"""
    logging.info(f"🔍 API /api/user called")
    logging.info(f"🔍 Session keys: {list(session.keys())}")
    logging.info(f"🔍 Has spotify_token: {'spotify_token' in session}")
    logging.info(f"🔍 Has user_info: {'user_info' in session}")
    logging.info(f"🔍 Session ID: {session.get('_permanent', 'Not permanent')}")
    
    # Add detailed session debugging
    if 'spotify_token' in session:
        token_expires = session.get('spotify_token_expires', 0)
        current_time = int(time.time())
        logging.info(f"🔍 Token expires: {token_expires}, Current time: {current_time}, Valid: {token_expires > current_time}")
    
    if not require_auth():
        logging.warning("❌ Authentication failed in /api/user")
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_info = session.get('user_info', {})
    logging.info(f"✅ User info retrieved successfully: {user_info.get('display_name', 'Unknown')}")
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

@app.route('/debug/session')
def debug_session():
    """Debug endpoint to check session state"""
    session_data = {
        'session_keys': list(session.keys()),
        'has_spotify_token': 'spotify_token' in session,
        'has_user_info': 'user_info' in session,
        'has_refresh_token': 'spotify_refresh_token' in session,
        'session_permanent': session.permanent,
        'environment': os.getenv('ENVIRONMENT'),
        'vercel': os.getenv('VERCEL'),
        'is_production': is_production,
        'user_info_content': session.get('user_info', {}),  # Show actual user_info content
        'spotify_scopes': SPOTIFY_SCOPES  # Show the scopes being requested
    }
    
    if 'spotify_token_expires' in session:
        session_data['token_expires'] = session['spotify_token_expires']
        session_data['current_time'] = int(time.time())
        session_data['token_valid'] = session['spotify_token_expires'] > int(time.time())
    
    return jsonify(session_data)

@app.route('/debug/token-test')
def debug_token_test():
    """Test current token permissions"""
    access_token = session.get('spotify_token')
    if not access_token:
        return jsonify({'error': 'No token available'}), 401
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Test different endpoints to check permissions
    results = {}
    
    try:
        # Test user info
        user_response = requests.get('https://api.spotify.com/v1/me', headers=headers, timeout=10)
        results['user_info'] = {
            'status': user_response.status_code,
            'data': user_response.json() if user_response.status_code == 200 else user_response.text
        }
        
        # Test playlists endpoint
        playlists_response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers, timeout=10)
        results['playlists'] = {
            'status': playlists_response.status_code,
            'can_read_playlists': playlists_response.status_code == 200
        }
        
        # Test create playlist (we'll just check if we can GET user ID for playlist creation)
        if user_response.status_code == 200:
            user_id = user_response.json().get('id')
            if user_id:
                # Test if we can access the user's profile (needed for playlist creation)
                profile_response = requests.get(f'https://api.spotify.com/v1/users/{user_id}', headers=headers, timeout=10)
                results['can_create_playlists'] = {
                    'status': profile_response.status_code,
                    'user_id': user_id,
                    'profile_accessible': profile_response.status_code == 200
                }
        
    except Exception as e:
        results['error'] = str(e)
    
    return jsonify(results)

@app.route('/debug/logout')
def debug_logout():
    """Force logout and clear session - useful for testing fresh auth"""
    session.clear()
    logging.info("🔄 Session cleared for fresh authentication")
    return jsonify({'message': 'Session cleared. You can now login with fresh permissions.'})

@app.route('/privacy-policy')
def privacy_policy():
    """Privacy Policy page required for Spotify app review"""
    return render_template_string(PRIVACY_POLICY_TEMPLATE)

@app.route('/terms-of-service')
def terms_of_service():
    """Terms of Service page required for Spotify app review"""
    return render_template_string(TERMS_OF_SERVICE_TEMPLATE)

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