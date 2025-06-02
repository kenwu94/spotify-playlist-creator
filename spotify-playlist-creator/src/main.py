import os
import sys
from flask import Flask, render_template_string, request, session, redirect, url_for
from dotenv import load_dotenv
import requests
import urllib.parse
import secrets

# Add the src directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.playlist_routes import playlist_bp
from routes.auth_routes import auth_bp
from templates.html_template import HTML_TEMPLATE
from templates.login_template import LOGIN_TEMPLATE
from services.spotify_service import SpotifyService

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='resources', static_url_path='/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# Spotify OAuth settings
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://127.0.0.1:5000/callback'
scopes = 'playlist-modify-public playlist-modify-private user-read-private user-read-email'

# Initialize Spotify service
spotify_service = SpotifyService()

# Register blueprints
app.register_blueprint(playlist_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

def require_auth():
    """Check if user is authenticated"""
    return session.get('spotify_authenticated', False) and session.get('access_token')

@app.route('/')
def index():
    # Check if user is authenticated
    if not require_auth():
        return redirect(url_for('login'))
    
    return render_template_string(HTML_TEMPLATE)

@app.route('/login')
def login():
    """Display login page"""
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/callback')
def spotify_callback():
    """Handle Spotify OAuth callback using the working logic"""
    print(f"🎯 Callback received with args: {request.args}")
    
    code = request.args.get('code')
    if code:
        try:
            # Use the working token exchange logic with detailed error handling
            token = get_user_token(code)
            user_info = get_user_info(token)
            
            # Store in session
            session['access_token'] = token
            session['spotify_authenticated'] = True
            session['user_info'] = user_info
            
            print("✅ Successfully authenticated with Spotify")
            return redirect(url_for('index'))
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error during token exchange: {e}")
            if e.response:
                print(f"❌ Response status: {e.response.status_code}")
                print(f"❌ Response content: {e.response.text}")
            return f"Authentication error: {e.response.text if e.response else str(e)}", 400
        except Exception as e:
            print(f"❌ General error during token exchange: {e}")
            return f"Authentication error: {e}", 400
    else:
        error = request.args.get('error')
        return f"Authorization failed: {error}", 400

def get_user_token(auth_code):
    """Get user access token using the working logic"""
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    # Debug: Print the request data (without sensitive info)
    print(f"🔍 Token exchange request:")
    print(f"   - URL: {url}")
    print(f"   - grant_type: {data['grant_type']}")
    print(f"   - redirect_uri: {data['redirect_uri']}")
    print(f"   - client_id: {data['client_id']}")
    print(f"   - client_secret: {data['client_secret'][:10]}..." if data['client_secret'] else "None")
    print(f"   - code: {auth_code[:30]}...")
    
    response = requests.post(url, headers=headers, data=data)
    
    # Debug: Print response details
    print(f"🔍 Token exchange response:")
    print(f"   - Status: {response.status_code}")
    print(f"   - Headers: {dict(response.headers)}")
    print(f"   - Content: {response.text}")
    
    response.raise_for_status()
    return response.json()["access_token"]

def get_user_info(token):
    """Get user info from Spotify API"""
    url = 'https://api.spotify.com/v1/me'
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__': 
    print("🚀 Starting Flask app at http://127.0.0.1:5000")
    print("🔗 OAuth callback: http://127.0.0.1:5000/callback")
    app.run(host='127.0.0.1', port=5000, debug=True)