import os
import sys
import time  # Add this import
from flask import Flask, render_template_string, request, session, redirect, url_for
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

# Custom formatter for better log organization
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors and better structure"""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        # Format the message
        return super().format(record)

# Configure enhanced logging
def setup_logging():
    """Setup organized logging with colors and sections"""
    
    # Create custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(
        '%(asctime)s │ %(levelname)s │ %(name)s │ %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (no colors)
    file_handler = logging.FileHandler('app.log')
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

# Initialize logging
setup_logging()

app = Flask(__name__, static_folder='resources', static_url_path='/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# Spotify OAuth settings - make sure these match your auth_routes.py
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'  # Keep consistent with auth_routes.py
SPOTIFY_SCOPES = 'playlist-modify-public playlist-modify-private user-read-private user-read-email'

# Initialize Spotify service
spotify_service = SpotifyService()

# Register blueprints
app.register_blueprint(playlist_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

def log_section(title, color='\033[94m'):  # Blue by default
    """Print a formatted section header"""
    reset = '\033[0m'
    separator = "─" * 60
    print(f"\n{color}┌{separator}┐{reset}")
    print(f"{color}│{title:^60}│{reset}")
    print(f"{color}└{separator}┘{reset}")

def log_subsection(title):
    """Print a formatted subsection"""
    print(f"\n\033[36m▼ {title}\033[0m")  # Cyan

def log_key_value(key, value, indent=2):
    """Print formatted key-value pairs"""
    spaces = " " * indent
    print(f"{spaces}\033[37m{key}:\033[0m {value}")  # White key, default value

def require_auth():
    """Check if user is authenticated"""
    return session.get('spotify_token') and session.get('user_info')  # Check for spotify_token, not access_token

@app.route('/')
def index():
    # Check if user is authenticated
    if not require_auth():
        logging.info("🔐 User not authenticated, redirecting to login")
        return redirect(url_for('login'))
    
    logging.info("✅ User authenticated, serving main page")
    return render_template_string(HTML_TEMPLATE)

@app.route('/login')
@rate_limit(max_requests=10, window_seconds=60, per='ip')
def login():
    """Display login page"""
    logging.info("📄 Serving login page")
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/callback')
@rate_limit(max_requests=5, window_seconds=60, per='ip')
def spotify_callback():
    """Handle Spotify OAuth callback using the working logic"""
    log_section("SPOTIFY OAUTH CALLBACK", '\033[95m')  # Magenta
    
    log_subsection("Request Details")
    log_key_value("Args received", dict(request.args))
    log_key_value("Remote IP", request.remote_addr)
    
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    # Check for errors in the callback
    if error:
        logging.error(f"❌ Spotify authorization error: {error}")
        return redirect(url_for('login'))  # Redirect to login on error
    
    if not code:
        logging.error("❌ No authorization code received")
        return redirect(url_for('login'))  # Redirect to login on error
    
    # Verify state parameter for security
    session_state = session.get('oauth_state')
    if not session_state or state != session_state:
        logging.error("❌ Invalid state parameter - possible CSRF attack")
        logging.error(f"📝 Expected state: {session_state}")
        logging.error(f"📝 Received state: {state}")
        return redirect(url_for('login'))  # Redirect to login on error
    
    logging.info(f"🔄 Exchanging authorization code for tokens...")
    
    try:
        # Exchange authorization code for access token
        token_url = 'https://accounts.spotify.com/api/token'
        
        # Prepare the request data
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }
        
        # Make the token exchange request
        token_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        logging.info(f"🔗 Making token request to: {token_url}")
        logging.info(f"📝 Request data: {{'grant_type': 'authorization_code', 'redirect_uri': '{SPOTIFY_REDIRECT_URI}', 'client_id': '{SPOTIFY_CLIENT_ID[:8] if SPOTIFY_CLIENT_ID else 'None'}...'}}")
        
        response = requests.post(token_url, data=token_data, headers=token_headers)
        
        logging.info(f"📡 Token response status: {response.status_code}")
        
        if response.status_code == 200:
            token_info = response.json()
            
            # Store tokens in session
            session['spotify_token'] = token_info['access_token']
            session['spotify_refresh_token'] = token_info.get('refresh_token')
            session['spotify_token_expires'] = int(time.time()) + token_info.get('expires_in', 3600)
            
            logging.info("✅ Successfully obtained Spotify access token")
            logging.info(f"🕐 Token expires in: {token_info.get('expires_in', 3600)} seconds")
            
            # Get user info and store it
            user_info = get_user_info(token_info['access_token'])
            if user_info:
                session['user_info'] = user_info
                logging.info(f"👤 Logged in user: {user_info.get('display_name', 'Unknown')}")
                
                # Clear the state from session
                session.pop('oauth_state', None)
                
                logging.info("🎉 Authentication successful, redirecting to home page")
                return redirect(url_for('index'))
            else:
                logging.error("❌ Failed to get user info")
                return redirect(url_for('login'))
        else:
            # Log the error response for debugging
            try:
                error_data = response.json()
            except:
                error_data = response.text
            
            logging.error(f"❌ OAuth token exchange failed with status {response.status_code}")
            logging.error(f"📄 Error response: {error_data}")
            
            return redirect(url_for('login'))
    
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Network error during token exchange: {str(e)}")
        return redirect(url_for('login'))
    except Exception as e:
        logging.error(f"❌ Unexpected error during OAuth callback: {str(e)}")
        import traceback
        logging.error(f"📄 Full traceback: {traceback.format_exc()}")
        return redirect(url_for('login'))

@app.errorhandler(429)
def rate_limit_exceeded(error):
    logging.warning("🚦 Rate limit exceeded")
    return render_template_string("""
    <div style="text-align: center; margin: 100px auto; max-width: 500px; font-family: Arial;">
        <h2>🚦 Slow down there!</h2>
        <p>You're making requests too quickly. Please wait a moment and try again.</p>
        <p><a href="javascript:history.back()">← Go back</a></p>
    </div>
    """), 429

def get_user_token(auth_code):
    """Get user access token using the working logic"""
    log_subsection("Token Exchange Request")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    
    # Debug: Print the request data (without sensitive info)
    log_key_value("URL", url)
    log_key_value("Grant type", data['grant_type'])
    log_key_value("Redirect URI", data['redirect_uri'])
    log_key_value("Client ID", f"{data['client_id'][:10]}..." if data['client_id'] else "None")
    log_key_value("Client secret", f"{data['client_secret'][:10]}..." if data['client_secret'] else "None")
    log_key_value("Auth code", f"{auth_code[:15]}...{auth_code[-10:]}")
    
    response = requests.post(url, headers=headers, data=data)
    
    # Debug: Print response details
    log_subsection("Token Exchange Response")
    log_key_value("Status", f"{response.status_code} {'✅' if response.status_code == 200 else '❌'}")
    log_key_value("Content type", response.headers.get('content-type', 'Unknown'))
    log_key_value("Response size", f"{len(response.text)} chars")
    
    if response.status_code != 200:
        log_key_value("Error content", response.text[:200])
    
    response.raise_for_status()
    return response.json()["access_token"]

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

if __name__ == '__main__': 
    log_section("SPOTIFY PLAYLIST CREATOR", '\033[92m')  # Bright green
    
    print("\n\033[94m🚀 Application Configuration:\033[0m")
    log_key_value("Server", "http://127.0.0.1:5000")
    log_key_value("OAuth callback", "http://127.0.0.1:5000/callback")
    log_key_value("Rate limiting", "✅ Enabled")
    log_key_value("OpenAI protection", "✅ Enabled")
    log_key_value("Debug mode", "✅ Enabled")
    log_key_value("Client ID", f"{SPOTIFY_CLIENT_ID[:10]}..." if SPOTIFY_CLIENT_ID else "❌ Missing")
    log_key_value("Client secret", "✅ Configured" if SPOTIFY_CLIENT_SECRET else "❌ Missing")
    
    print(f"\n\033[93m📋 Available endpoints:\033[0m")
    log_key_value("Main app", "/")
    log_key_value("Login", "/login")
    log_key_value("OAuth callback", "/callback")
    log_key_value("Create playlist", "/create-playlist")
    log_key_value("Rate limit status", "/rate-limit-status")
    
    print(f"\n\033[96m🔧 Starting Flask development server...\033[0m\n")
    
    app.run(host='127.0.0.1', port=5000, debug=True)