from flask import Blueprint, request, jsonify
from core.playlist_creator import PlaylistCreator

# Create blueprint for playlist routes
playlist_bp = Blueprint('playlist', __name__)

# Initialize the playlist creator
playlist_creator = PlaylistCreator()

@playlist_bp.route('/create-playlist', methods=['POST'])
def create_playlist_endpoint():
    try:
        data = request.get_json()
        user_prompt = data.get('prompt')
        playlist_name = data.get('playlist_name')
        
        if not user_prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Create the playlist with detailed analysis
        result = playlist_creator.create_playlist_from_prompt(user_prompt, playlist_name)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error creating playlist: {e}")
        return jsonify({"error": str(e)}), 500

@playlist_bp.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "AI Spotify Playlist Creator is running!"})