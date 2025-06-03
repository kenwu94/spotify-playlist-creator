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
        token_data = {        'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }
        
        token_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(token_url, data=token_data, headers=token_headers)
        
        if response.status_code == 200:
            token_info = response.json()
            
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
                logging.error("❌ Failed to get user info")
                return redirect(url_for('index'))
        else:
            logging.error(f"❌ Token exchange failed: {response.status_code}")
            return redirect(url_for('index'))
    
    except Exception as e:
        logging.error(f"❌ OAuth callback error: {str(e)}")
        return redirect(url_for('index'))

def get_user_info(access_token):
    """Get user information from Spotify"""
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"❌ Failed to get user info: {response.status_code}")
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