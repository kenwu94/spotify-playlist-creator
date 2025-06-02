import os
import requests
from urllib.parse import quote
import random
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.scope = "playlist-modify-public playlist-modify-private user-read-private user-read-email"
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def authenticate(self):
        """Authenticate with Spotify using Client Credentials flow for searching"""
        try:
            url = "https://accounts.spotify.com/api/token"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }

            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            response_data = response.json()
            self.search_token = response_data["access_token"]
            
            print("✅ Successfully authenticated with Spotify API for searching")
            return True
            
        except Exception as e:
            print(f"❌ Failed to authenticate with Spotify: {e}")
            return False
    
    def get_user_id(self, token):
        """Get user ID from access token"""
        url = 'https://api.spotify.com/v1/me'
        headers = {'Authorization': f'Bearer {token}'}
        
        # Use the provided token directly, not the search token
        response = requests.get(url, headers=headers)
        
        # If 401, the user token has expired and needs to be refreshed via OAuth
        if response.status_code == 401:
            raise Exception("User access token expired - user needs to re-authenticate")
            
        response.raise_for_status()
        return response.json()['id']
    
    def search_for_song(self, token, song_name, artist_name, search_type="track"):
        """Search for a song using the working logic"""
        if not song_name or not artist_name:
            return None
            
        query = f"track:{song_name} artist:{artist_name}"
        encoded_query = quote(query)
        url = f"https://api.spotify.com/v1/search?q={encoded_query}&type={search_type}&limit=1"

        headers = {"Authorization": f"Bearer {token}"}

        response = self.make_authenticated_request('GET', url, headers=headers)
        response.raise_for_status()
        result = response.json()
        tracks = result.get('tracks', {}).get('items', [])
        if tracks:
            return tracks[0]['id']  # Return track ID
        return None

    def get_ai_generated_songs(self, analysis, max_songs=30):
        """Use OpenAI to generate diverse, contextually relevant song recommendations"""
        try:
            prompt = self.build_openai_song_prompt(analysis, max_songs)
            
            print("🤖 Asking OpenAI for song recommendations...")
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a music expert and DJ with deep knowledge of songs across all genres, decades, and cultures. You create diverse, interesting playlists that introduce people to both popular and lesser-known gems."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.8  # Higher temperature for more creative/diverse suggestions
            )
            
            ai_response = response.choices[0].message.content
            print(f"🎵 OpenAI suggested songs for: {analysis.get('mood', 'unknown mood')}")
            
            # Parse the AI response to extract songs
            song_suggestions = self.parse_ai_song_response(ai_response)
            
            # Search for these songs on Spotify
            found_songs = self.search_ai_suggested_songs(song_suggestions)
            
            return found_songs
            
        except Exception as e:
            print(f"❌ Error getting AI song recommendations: {e}")
            # Fallback to basic search if AI fails
            return self.get_fallback_songs(analysis, max_songs)

    def build_openai_song_prompt(self, analysis, max_songs):
        """Build a detailed prompt for OpenAI to generate song recommendations"""
        mood = analysis.get('mood', 'neutral')
        genres = analysis.get('genres', [])
        energy = analysis.get('energy', 'medium')
        themes = analysis.get('themes', [])
        keywords = analysis.get('keywords', [])
        original_prompt = analysis.get('original_prompt', '')
        
        prompt = f"""
Based on this analysis of a user's music request, recommend exactly {max_songs} diverse songs:

MOOD: {mood}
ENERGY LEVEL: {energy}
PREFERRED GENRES: {', '.join(genres) if genres else 'Any'}
THEMES: {', '.join(themes) if themes else 'General'}
KEY WORDS: {', '.join(keywords) if keywords else 'None'}
ORIGINAL REQUEST: "{original_prompt[:200]}..."

Please provide exactly {max_songs} song recommendations that:
1. Match the mood and energy level perfectly
2. Include a diverse mix of:
   - Popular hits and hidden gems
   - Different decades (70s, 80s, 90s, 2000s, 2010s, 2020s)
   - Various genres and subgenres
   - Different artists (no more than 2 songs per artist)
   - International music when appropriate
3. Create a cohesive emotional journey
4. Include both mainstream and alternative/indie options

IMPORTANT: You must provide exactly {max_songs} songs, no more, no less.

For each song, provide:
- Song title
- Artist name
- Brief reason why it fits

Format your response as a JSON array like this:
[
  {{
    "song": "Song Title",
    "artist": "Artist Name", 
    "reason": "Why this song fits the mood/theme"
  }}
]

Focus on creating a playlist that would genuinely resonate with someone feeling this way, not just obvious keyword matches.
"""
        return prompt

    def parse_ai_song_response(self, ai_response):
        """Parse OpenAI's response to extract song recommendations"""
        try:
            # Try to extract JSON from the response
            start_idx = ai_response.find('[')
            end_idx = ai_response.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                songs = json.loads(json_str)
                
                # Validate the structure
                validated_songs = []
                for song in songs:
                    if isinstance(song, dict) and 'song' in song and 'artist' in song:
                        validated_songs.append({
                            'name': song['song'].strip(),
                            'artist': song['artist'].strip(),
                            'reason': song.get('reason', 'AI recommendation'),
                            'source': 'openai_generated'
                        })
                
                print(f"✅ Parsed {len(validated_songs)} song suggestions from OpenAI")
                return validated_songs
                
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON from AI response: {e}")
        except Exception as e:
            print(f"❌ Error parsing AI response: {e}")
        
        # Fallback: try to extract songs manually
        return self.manual_parse_ai_response(ai_response)

    def manual_parse_ai_response(self, ai_response):
        """Manually parse AI response if JSON parsing fails"""
        songs = []
        lines = ai_response.split('\n')
        
        current_song = {}
        for line in lines:
            line = line.strip()
            
            # Look for patterns like "Song: Title" or "Artist: Name"
            if line.lower().startswith(('song:', '"song":', 'title:')):
                title = line.split(':', 1)[1].strip().strip('"')
                current_song['name'] = title
            elif line.lower().startswith(('artist:', '"artist":')):
                artist = line.split(':', 1)[1].strip().strip('"')
                current_song['artist'] = artist
            elif line.lower().startswith(('reason:', '"reason":')):
                reason = line.split(':', 1)[1].strip().strip('"')
                current_song['reason'] = reason
                
                # If we have both song and artist, add it
                if 'name' in current_song and 'artist' in current_song:
                    current_song['source'] = 'openai_manual_parse'
                    songs.append(current_song.copy())
                    current_song = {}
            
            # Also look for simple patterns like "1. Artist - Song"
            elif line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering and dashes
                clean_line = line.lstrip('0123456789.- ')
                if ' - ' in clean_line:
                    parts = clean_line.split(' - ', 1)
                    if len(parts) == 2:
                        songs.append({
                            'name': parts[1].strip(),
                            'artist': parts[0].strip(),
                            'reason': 'AI recommendation',
                            'source': 'openai_pattern_match'
                        })
        
        print(f"✅ Manually parsed {len(songs)} songs from AI response")
        return songs

    def search_ai_suggested_songs(self, song_suggestions):
        """Search for AI-suggested songs on Spotify"""
        if not hasattr(self, 'search_token'):
            self.authenticate()
            
        found_songs = []
        search_token = getattr(self, 'search_token', None)
        
        if not search_token:
            print("❌ No search token available")
            return found_songs
        
        for suggestion in song_suggestions:
            try:
                song_name = suggestion.get('name', '')
                artist_name = suggestion.get('artist', '')
                reason = suggestion.get('reason', 'AI recommendation')
                
                if not song_name or not artist_name:
                    continue
                
                # Try exact search first
                song_id = self.search_for_song(search_token, song_name, artist_name)
                
                # If exact search fails, try broader search
                if not song_id:
                    song_id = self.fuzzy_search_song(search_token, song_name, artist_name)
                
                if song_id:
                    found_songs.append({
                        'id': song_id,
                        'name': song_name,
                        'artist': artist_name,
                        'reason': reason,
                        'source': 'ai_recommendation',
                        'genre': 'AI Selected'
                    })
                    print(f"✅ Found AI suggestion: {song_name} by {artist_name}")
                else:
                    print(f"❌ Not found on Spotify: {song_name} by {artist_name}")
                    
            except Exception as e:
                print(f"❌ Error searching for {suggestion.get('name', 'unknown')}: {e}")
                continue
        
        print(f"🎵 Successfully found {len(found_songs)} AI-recommended songs on Spotify")
        return found_songs

    def fuzzy_search_song(self, token, song_name, artist_name):
        """Try a broader search if exact match fails"""
        try:
            # Try just the song name
            query = f'"{song_name}"'
            encoded_query = quote(query)
            url = f"https://api.spotify.com/v1/search?q={encoded_query}&type=track&limit=5"
            
            headers = {"Authorization": f"Bearer {token}"}
            response = self.make_authenticated_request('GET', url, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            tracks = result.get('tracks', {}).get('items', [])
            
            # Look for the artist in the results
            for track in tracks:
                track_artists = [artist['name'].lower() for artist in track['artists']]
                if any(artist_name.lower() in track_artist for track_artist in track_artists):
                    return track['id']
            
            # If still no match, return the first result
            if tracks:
                return tracks[0]['id']
                
        except Exception as e:
            print(f"❌ Fuzzy search failed for {song_name}: {e}")
        
        return None

    def get_fallback_songs(self, analysis, max_songs):
        """Fallback method if AI recommendations fail"""
        print("🔄 Using fallback song discovery method...")
        
        # Use a simple genre-based search as fallback
        genres = analysis.get('genres', ['pop', 'rock'])
        mood = analysis.get('mood', 'neutral')
        
        fallback_songs = []
        search_token = getattr(self, 'search_token', None)
        
        if not search_token:
            return fallback_songs
        
        for genre in genres[:3]:  # Try up to 3 genres
            try:
                query = f"genre:{genre}"
                encoded_query = quote(query)
                url = f"https://api.spotify.com/v1/search?q={encoded_query}&type=track&limit=10"
                
                headers = {"Authorization": f"Bearer {search_token}"}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                result = response.json()
                tracks = result.get('tracks', {}).get('items', [])
                
                for track in tracks[:5]:  # Take 5 from each genre
                    fallback_songs.append({
                        'id': track['id'],
                        'name': track['name'],
                        'artist': ', '.join([artist['name'] for artist in track['artists']]),
                        'reason': f'Fallback - {genre} genre match',
                        'source': 'fallback_search',
                        'genre': genre
                    })
                    
            except Exception as e:
                print(f"❌ Fallback search failed for {genre}: {e}")
                continue
        
        return fallback_songs[:max_songs]

    def refresh_token_if_needed(self, response):
        """Check if token needs refresh and handle it"""
        if response.status_code == 401:
            print("🔄 Token expired, refreshing...")
            if self.authenticate():
                return True
        return False

    def make_authenticated_request(self, method, url, headers=None, **kwargs):
        """Make request with automatic token refresh"""
        if headers is None:
            headers = {}
        
        # Add authorization header
        if hasattr(self, 'search_token'):
            headers['Authorization'] = f'Bearer {self.search_token}'
        
        # Make initial request
        response = requests.request(method, url, headers=headers, **kwargs)
        
        # If unauthorized, try to refresh token and retry
        if response.status_code == 401:
            if self.refresh_token_if_needed(response):
                headers['Authorization'] = f'Bearer {self.search_token}'
                response = requests.request(method, url, headers=headers, **kwargs)
        
        return response

    # Keep existing methods
    def create_playlist(self, access_token, playlist_name, description, song_ids):
        """Create a Spotify playlist using the working logic"""
        try:
            # Get user ID using the provided access token
            user_id = self.get_user_id(access_token)
            
            print(f"🎵 Creating playlist '{playlist_name}' for user {user_id}")
            
            # Create the playlist
            url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "name": playlist_name,
                "description": description,
                "public": True
            }
            
            # Use requests directly with the user token
            response = requests.post(url, headers=headers, json=data)
            
            # If 401, the user token has expired
            if response.status_code == 401:
                raise Exception("User access token expired - user needs to re-authenticate")
                
            response.raise_for_status()
            playlist = response.json()
            
            # Add tracks to playlist if provided
            if song_ids:
                valid_song_ids = [sid for sid in song_ids if sid]  # Filter out None/empty IDs
                track_uris = [f"spotify:track:{track_id}" for track_id in valid_song_ids]
                
                if track_uris:
                    print(f"🎵 Adding {len(track_uris)} tracks to playlist...")
                    # Add tracks in batches of 100
                    for i in range(0, len(track_uris), 100):
                        batch = track_uris[i:i+100]
                        self.add_tracks_to_playlist(access_token, playlist['id'], batch)
            
            print(f"✅ Successfully created playlist with {len([sid for sid in song_ids if sid])} songs")
            
            return {
                "playlist_id": playlist['id'],
                "playlist_url": playlist['external_urls']['spotify'],
                "name": playlist['name'],
                "description": playlist['description'],
                "track_count": len([sid for sid in song_ids if sid]),
                "success": True
            }
            
        except Exception as e:
            print(f"❌ Error creating playlist: {e}")
            return {"error": str(e), "success": False}

    def add_tracks_to_playlist(self, token, playlist_id, track_uris, position=0):
        """Add tracks to playlist using the working logic"""
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "uris": track_uris,
            "position": position
        }
        
        # Use requests directly with the user token
        response = requests.post(url, headers=headers, json=data)
        
        # If 401, the user token has expired
        if response.status_code == 401:
            raise Exception("User access token expired - user needs to re-authenticate")
            
        response.raise_for_status()
        return response.json()

    def search_songs(self, songs_data, max_songs=50):
        """Search for multiple songs and return their IDs"""
        if not hasattr(self, 'search_token'):
            self.authenticate()
            
        found_songs = []
        search_token = getattr(self, 'search_token', None)
        
        for song in songs_data[:max_songs]:
            try:
                song_id = self.search_for_song(search_token, song['name'], song['artist'])
                if song_id:
                    found_songs.append({
                        'id': song_id,
                        'name': song['name'],
                        'artist': song['artist'],
                        'genre': song.get('genre', 'Unknown')
                    })
                    print(f"✅ Found: {song['name']} by {song['artist']}")
                else:
                    print(f"❌ Not found: {song['name']} by {song['artist']}")
            except Exception as e:
                print(f"❌ Error searching for {song['name']}: {e}")
                continue
                
        return found_songs

    # Keep your existing methods for generating songs from analysis
    def _build_search_queries(self, analysis):
        """Build search queries based on sentiment analysis"""
        # Your existing implementation here
        pass

    def _search_with_fallback(self, queries, limit_per_query=10):
        """Search with fallback options"""
        # Your existing implementation here
        pass

    def generate_playlist_name(self, prompt, analysis):
        """Generate a creative playlist name using OpenAI based on the prompt and analysis"""
        try:
            name_prompt = f"""
            Create a creative, catchy playlist name (2-6 words max) based on this user prompt and analysis:
            
            User Prompt: "{prompt}"
            
            Analysis:
            - Primary Mood: {analysis.get('primary_mood', 'unknown')}
            - Genres: {', '.join(analysis.get('genre_suggestions', [])[:3])}
            - Energy: {analysis.get('energy_level', 'medium')}
            - Time Period: {analysis.get('time_period', 'any')}
            - Activity: {analysis.get('activity', 'listening')}
            - Emotions: {', '.join(analysis.get('emotions', [])[:3])}
            
            Guidelines:
            - Keep it short and memorable (2-6 words)
            - Make it emotionally resonant
            - Can be poetic, fun, or descriptive
            - Avoid generic names like "My Playlist"
            - Can use emojis sparingly (1-2 max)
            
            Examples of good names:
            - "Midnight Melancholy"
            - "Summer Drive Vibes"
            - "Heartbreak Anthems"
            - "3AM Thoughts"
            - "Golden Hour Dreams"
            - "Rainy Day Refuge"
            
            Return ONLY the playlist name, nothing else.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a creative playlist naming expert. Generate short, catchy, emotionally resonant playlist names."},
                    {"role": "user", "content": name_prompt}
                ],
                max_tokens=50,
                temperature=0.8  # Higher temperature for more creativity
            )
            
            generated_name = response.choices[0].message.content.strip()
            # Clean up the name (remove quotes if present)
            generated_name = generated_name.strip('"\'')
            
            print(f"🎨 Generated playlist name: '{generated_name}'")
            return generated_name
            
        except Exception as e:
            print(f"❌ Error generating playlist name: {e}")
            # Fallback to a simple generated name
            mood = analysis.get('primary_mood', 'Mixed')
            genre = analysis.get('genre_suggestions', ['Music'])[0] if analysis.get('genre_suggestions') else 'Music'
            return f"{mood.title()} {genre.title()} Mix"