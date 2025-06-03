from flask import Blueprint, request, redirect, session, url_for, jsonify
import urllib.parse
import secrets
import os

auth_bp = Blueprint('auth', __name__)

# Spotify OAuth settings
client_id = os.getenv('SPOTIFY_CLIENT_ID')

# Use the same redirect URI logic as main.py
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:5000/callback')
print(f"🔗 Using redirect URI: {redirect_uri}")

scopes = 'playlist-modify-public playlist-modify-private user-read-private user-read-email user-top-read user-read-recently-played user-library-read user-follow-read'

@auth_bp.route('/login')
def login():
    """Redirect user to Spotify authorization"""
    state = secrets.token_urlsafe(16)
    
    # Store the state in session for verification in callback
    session['oauth_state'] = state
    
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scopes,
        'redirect_uri': redirect_uri,
        'state': state,
        'show_dialog': 'true'
    }
    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params)
    return redirect(url)

@auth_bp.route('/logout')
def logout():
    """Clear session and redirect to login page"""
    session.clear()
    return redirect(url_for('login_page'))  # Changed from 'index' to 'login_page'

@auth_bp.route('/user-info')
def user_info():
    """Get current user info with token refresh if needed"""
    access_token = session.get('spotify_token')
    if not access_token:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Check token expiration
    token_expires = session.get('spotify_token_expires', 0)
    if token_expires < (int(time.time()) + 300):  # Refresh if expires within 5 minutes
        if not refresh_user_token():
            return jsonify({'error': 'Session expired'}), 401
    
    return jsonify(session.get('user_info', {}))

def refresh_user_token():
    """Refresh the user's access token using the refresh token"""
    refresh_token = session.get('spotify_refresh_token')
    
    if not refresh_token:
        return False
    
    try:
        import time
        import requests
        
        SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
        
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
            
            return True
        else:
            return False
            
    except Exception as e:
        return False