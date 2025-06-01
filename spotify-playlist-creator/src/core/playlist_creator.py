from services.sentiment_analyzer import SentimentAnalyzer
from services.spotify_service import SpotifyService

class PlaylistCreator:
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.spotify_service = SpotifyService()
    
    def create_playlist_from_prompt(self, user_prompt, playlist_name=None):
        """Main method to create playlist from user input"""
        print(f"🎯 Analyzing prompt: '{user_prompt[:50]}...'")
        
        # Step 1: Analyze the prompt with OpenAI (now with detailed analysis)
        analysis = self.sentiment_analyzer.analyze_prompt(user_prompt)
        print(f"✅ Analysis complete - Primary Mood: {analysis['primary_mood']}, Energy: {analysis['energy_level']}, Detail Level: {analysis.get('detail_level', 'basic')}")
        
        # Step 2: Authenticate with Spotify
        if not self.spotify_service.authenticate():
            raise Exception("Failed to authenticate with Spotify")
        
        # Step 3: Search for songs based on detailed analysis
        songs = self.spotify_service.search_songs(analysis)
        print(f"✅ Found {len(songs)} songs matching the detailed criteria")
        
        # Step 4: Create playlist name if not provided
        if not playlist_name:
            mood = analysis['primary_mood']
            activity = analysis.get('activity', '')
            setting = analysis.get('setting', '')
            
            if activity and activity != 'general listening' and activity != 'any':
                playlist_name = f"AI Playlist - {mood.title()} {activity.title()}"
            elif setting and setting != 'any':
                playlist_name = f"AI Playlist - {mood.title()} at {setting.title()}"
            else:
                playlist_name = f"AI Playlist - {mood.title()}"
        
        # Step 5: Create the playlist
        song_ids = [song['id'] for song in songs]
        playlist = self.spotify_service.create_playlist(
            user_id="placeholder_user_id",
            playlist_name=playlist_name,
            description=analysis['playlist_description'],
            song_ids=song_ids
        )
        
        return {
            "analysis": analysis,
            "songs": songs,
            "playlist": playlist
        }