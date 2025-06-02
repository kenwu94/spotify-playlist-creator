from flask import Blueprint, request, jsonify, session
from services.openai_service import OpenAIService
from services.spotify_service import SpotifyService
from services.rate_limiter import rate_limit, openai_rate_limit
import logging
import traceback

# Create blueprint for playlist routes
playlist_bp = Blueprint('playlist', __name__)

@playlist_bp.route('/create-playlist', methods=['POST'])
@rate_limit(max_requests=5, window_seconds=60, per='ip')  # General rate limit
@openai_rate_limit(estimated_tokens=2000, model="gpt-4")  # OpenAI specific limit
def create_playlist():
    """Create a playlist with optional user preferences"""
    try:
        # Check authentication - use the same keys as main.py
        if not session.get('spotify_token') or not session.get('user_info'):
            logging.error("❌ User not authenticated")
            return jsonify({'error': 'Not authenticated with Spotify'}), 401
        
        # Get the access token from session
        access_token = session.get('spotify_token')
        
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        playlist_name = data.get('playlist_name', '').strip()
        song_count = data.get('song_count', 20)
        use_preferences = data.get('use_preferences', False)  # New option
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Log the request for monitoring
        logging.info(f"🎵 Playlist creation request: {len(prompt)} chars, {song_count} songs, preferences: {use_preferences}")
        logging.info(f"📝 Prompt content: {prompt[:100]}...")
        
        # Initialize services
        openai_service = OpenAIService()
        spotify_service = SpotifyService()
        
        # Get user preferences if requested
        user_preferences = {}
        if use_preferences:
            logging.info("🔍 Getting user listening preferences...")
            user_preferences = spotify_service.get_user_preferences(access_token)
            if user_preferences:
                logging.info(f"✅ Found preferences: {len(user_preferences.get('favorite_artists', []))} artists, {len(user_preferences.get('favorite_genres', []))} genres")
            else:
                logging.warning("⚠️ No user preferences found")
        
        # Analyze prompt with OpenAI (include user preferences)
        logging.info("🤖 Starting OpenAI analysis...")
        analysis = openai_service.analyze_prompt(prompt, user_preferences if use_preferences else None)
        logging.info(f"✅ OpenAI analysis completed: {type(analysis)}")
        
        # Add the original prompt to analysis for better song generation
        analysis['original_prompt'] = prompt
        analysis['used_preferences'] = use_preferences
        if use_preferences and user_preferences:
            analysis['user_preferences_summary'] = {
                'top_artists': user_preferences.get('favorite_artists', [])[:5],
                'top_genres': user_preferences.get('favorite_genres', [])[:5],
                'audio_profile': user_preferences.get('audio_preferences', {})
            }
        
        # Use the AI-powered song generation method that already exists
        logging.info("🎵 Starting AI-powered Spotify search...")
        songs = spotify_service.get_ai_generated_songs(analysis, song_count)
        logging.info(f"✅ Found {len(songs) if songs else 0} songs")
        
        if not songs:
            return jsonify({'error': 'No songs found matching your criteria'}), 404
        
        # Extract song IDs for playlist creation
        song_ids = [song['id'] for song in songs if song.get('id')]
        
        # Generate playlist name if not provided
        if not playlist_name:
            playlist_name = spotify_service.generate_playlist_name(prompt, analysis)
        
        # Generate playlist description
        description = f"AI-generated playlist based on: {prompt[:100]}..."
        if use_preferences:
            description += " (Personalized with your listening history)"
        
        # Create playlist using the correct method signature
        logging.info("🎵 Creating playlist on Spotify...")
        playlist_result = spotify_service.create_playlist(
            access_token,  # access_token first
            playlist_name,
            description,
            song_ids
        )
        
        if not playlist_result.get('success', False):
            return jsonify({'error': f'Failed to create playlist: {playlist_result.get("error", "Unknown error")}'}), 500
        
        logging.info("🎉 Playlist created successfully")
        
        return jsonify({
            'playlist': playlist_result,
            'songs': songs,
            'analysis': analysis,
            'success': True
        })
        
    except Exception as e:
        logging.error(f"❌ Error creating playlist: {str(e)}")
        logging.error(f"📄 Full traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@playlist_bp.route('/rate-limit-status')
def rate_limit_status():
    """Get current rate limit status"""
    from services.rate_limiter import openai_rate_limiter
    return jsonify(openai_rate_limiter.get_status())