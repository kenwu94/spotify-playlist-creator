from flask import Blueprint, request, jsonify, session, redirect, url_for
from services.sentiment_analyzer import SentimentAnalyzer
from services.spotify_service import SpotifyService
import traceback

# Create blueprint for playlist routes
playlist_bp = Blueprint('playlist', __name__)

def require_auth():
    """Check if user is authenticated"""
    return session.get('spotify_authenticated', False) and session.get('access_token')

@playlist_bp.route('/create-playlist', methods=['POST'])
def create_playlist():
    # Check authentication first
    if not require_auth():
        return jsonify({
            'error': 'Authentication required',
            'redirect': '/login'
        }), 401
    
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        playlist_name = data.get('playlist_name', '').strip()
        song_count = data.get('song_count', 25)  # Default to 25 songs
        
        # Validate song count
        try:
            song_count = int(song_count)
            if song_count < 10 or song_count > 50:
                return jsonify({'error': 'Song count must be between 10 and 50'}), 400
        except (ValueError, TypeError):
            song_count = 25  # Default fallback
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        print(f"🎵 Creating AI-powered playlist for prompt: {prompt[:100]}...")
        
        # Initialize services
        sentiment_analyzer = SentimentAnalyzer()
        spotify_service = SpotifyService()
        
        # Authenticate Spotify for searching
        if not spotify_service.authenticate():
            return jsonify({'error': 'Failed to authenticate with Spotify'}), 500
        
        # Analyze the prompt using sentiment analyzer
        print(f"🧠 Analyzing sentiment and extracting metadata for {song_count} songs...")
        analysis = sentiment_analyzer.analyze_prompt(prompt)
        
        # Add the original prompt to analysis for OpenAI context
        analysis['original_prompt'] = prompt
        
        # Generate playlist name if not provided
        if not playlist_name:
            print("🎨 Generating AI playlist name...")
            playlist_name = spotify_service.generate_playlist_name(prompt, analysis)
        
        # Get AI-generated songs with the specified count
        print(f"🎵 Getting {song_count} AI-generated song recommendations...")
        songs = spotify_service.get_ai_generated_songs(analysis, max_songs=song_count)
        
        # Check if user is authenticated for playlist creation
        access_token = session.get('access_token')
        if access_token:
            # User is logged in - create real playlist
            song_ids = [song['id'] for song in songs if song.get('id')]
            description = prompt
            
            playlist_result = spotify_service.create_playlist(
                access_token, 
                playlist_name, 
                description, 
                song_ids
            )
            
            if playlist_result.get('success'):
                return jsonify({
                    'analysis': analysis,
                    'songs': songs,
                    'playlist': playlist_result,
                    'message': f'Successfully created AI-curated playlist "{playlist_name}" with {len(song_ids)} songs!',
                    'ai_info': {
                        'total_suggestions': len(songs),
                        'found_on_spotify': len(song_ids),
                        'powered_by': 'OpenAI GPT-4 + Spotify'
                    }
                })
            else:
                return jsonify({
                    'analysis': analysis,
                    'songs': songs,
                    'playlist': {
                        'name': playlist_name,
                        'description': description,
                        'error': playlist_result.get('error', 'Failed to create playlist'),
                        'playlist_url': '#'
                    }
                })
        else:
            # User not logged in - return preview
            return jsonify({
                'analysis': analysis,
                'songs': songs,
                'playlist': {
                    'name': playlist_name,
                    'description': prompt,
                    'playlist_url': '#login-required',
                    'note': 'Login to Spotify to create this AI-curated playlist',
                    'preview_count': len(songs)
                },
                'ai_info': {
                    'total_suggestions': len(songs),
                    'powered_by': 'OpenAI GPT-4 + Spotify'
                }
            })
        
    except Exception as e:
        print(f"❌ Error creating playlist: {e}")
        print(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500