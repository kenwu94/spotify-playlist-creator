from flask import Blueprint, request, redirect, session, url_for, jsonify
import urllib.parse
import secrets
import os

auth_bp = Blueprint('auth', __name__)

# Spotify OAuth settings
client_id = os.getenv('SPOTIFY_CLIENT_ID')
redirect_uri = 'http://127.0.0.1:5000/callback'
scopes = 'playlist-modify-public playlist-modify-private user-read-private user-read-email'

@auth_bp.route('/login')
def login():
    """Redirect user to Spotify authorization using the working logic"""
    state = secrets.token_urlsafe(16)
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scopes,
        'redirect_uri': redirect_uri,
        'state': state,
        'show_dialog': 'true'
    }
    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params)
    print(f"🔗 Redirecting to: {url}")
    return redirect(url)

@auth_bp.route('/logout')
def logout():
    """Clear session and redirect to login"""
    session.clear()
    return redirect(url_for('login'))

@auth_bp.route('/user-info')
def user_info():
    """Get current user info"""
    if not session.get('spotify_authenticated'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify(session.get('user_info', {}))