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
    """Get current user info"""
    if not session.get('spotify_token'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify(session.get('user_info', {}))