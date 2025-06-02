import openai
import os
import json
import logging
from services.rate_limiter import openai_rate_limiter

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def analyze_prompt(self, prompt, user_preferences=None):
        """Analyze a user prompt and return detailed music characteristics with optional user preferences"""
        
        # Build the system message with user preferences if available
        system_message = """You are a music analyst that converts descriptions into specific musical characteristics for playlist creation."""
        
        preference_context = ""
        if user_preferences:
            preference_context = self.format_user_preferences_for_context(user_preferences)
            system_message += f"\n\nUser's Musical Profile:\n{preference_context}"
            system_message += "\n\nWhen analyzing their request, consider how it might relate to their established preferences, but prioritize their current mood/request."
        
        # Build the user message
        user_message = f"""
        Analyze this description and provide detailed musical characteristics: "{prompt}"
        
        Provide a JSON response with these exact fields:
        {{
            "primary_mood": "string (e.g., melancholic, energetic, peaceful)",
            "secondary_moods": ["array", "of", "mood", "strings"],
            "emotions": ["array", "of", "emotions"],
            "valence": "string (high/medium/low happiness level)",
            "genre_suggestions": ["array", "of", "main", "genres"],
            "subgenres": ["array", "of", "specific", "subgenres"],
            "tempo": "string (slow/medium/fast or specific BPM range)",
            "energy_level": "string (low/medium/high)",
            "danceability": "string (low/medium/high)",
            "instrumentalness": "string (vocal/mixed/instrumental preference)",
            "acousticness": "string (acoustic/mixed/electronic preference)",
            "time_period": "string (e.g., 2020s, 1980s, 1990s-2000s, any)",
            "themes": ["array", "of", "lyrical", "themes"],
            "language": "string (e.g., english, spanish, any)",
            "popularity": "string (mainstream/underground/mixed)",
            "complexity": "string (simple/moderate/complex)",
            "time_of_day": "string (morning/afternoon/evening/night/any)",
            "season": "string (spring/summer/fall/winter/any)",
            "weather": "string (sunny/rainy/cloudy/any)",
            "activity": "string (working out/studying/relaxing/party/driving/any)",
            "setting": "string (home/car/gym/party/outdoor/any)",
            "vocal_style": "string (soft/powerful/raspy/smooth/any)",
            "instruments": ["array", "of", "prominent", "instruments"],
            "lyrical_content": ["array", "of", "content", "types"],
            "detail_level": "string (basic/detailed/comprehensive)"
        }}
        """
        
        # Analyze prompt with built-in rate limiting and cost estimation
        # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
        estimated_prompt_tokens = len(prompt) // 4 + 1000  # Add buffer for system prompt
        estimated_completion_tokens = 800  # Estimated response size
        
        # Check rate limits before making the call
        allowed, error_msg = openai_rate_limiter.is_allowed(
            estimated_tokens=estimated_prompt_tokens + estimated_completion_tokens,
            model="gpt-3.5-turbo"
        )
        
        if not allowed:
            raise Exception(f"Rate limit exceeded: {error_msg}")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Get the response content
            content = response.choices[0].message.content
            
            # Log the raw response for debugging
            logging.info(f"OpenAI raw response: {content[:200]}...")
            
            # Validate that we got content
            if not content or content.strip() == "":
                logging.error("OpenAI returned empty content")
                raise Exception("OpenAI returned empty response")
            
            # Log actual token usage for monitoring
            usage = response.usage
            actual_cost = openai_rate_limiter.estimate_cost(
                usage.prompt_tokens, 
                usage.completion_tokens, 
                "gpt-3.5-turbo"
            )
            
            logging.info(f"OpenAI API call: {usage.prompt_tokens} + {usage.completion_tokens} tokens, ${actual_cost:.4f}")
            
            # Try to parse JSON, with fallback
            try:
                # Clean the content - remove any markdown code blocks
                clean_content = content.strip()
                if clean_content.startswith("```json"):
                    clean_content = clean_content[7:]
                if clean_content.endswith("```"):
                    clean_content = clean_content[:-3]
                clean_content = clean_content.strip()
                
                analysis = json.loads(clean_content)
                
                # Validate required fields and add defaults if missing
                analysis = self._validate_and_fix_analysis(analysis)
                
                # Add user preferences summary to analysis
                if user_preferences:
                    analysis['user_preferences_summary'] = {
                        'top_artists': user_preferences.get('favorite_artists', [])[:5],
                        'top_genres': user_preferences.get('favorite_genres', [])[:5],
                        'audio_profile': user_preferences.get('audio_preferences', {})
                    }
                    analysis['used_preferences'] = True
                else:
                    analysis['used_preferences'] = False
                
                return analysis
                
            except json.JSONDecodeError as e:
                logging.error(f"JSON parsing error: {e}")
                logging.error(f"Raw content: {content}")
                
                # Return a fallback analysis based on the prompt
                return self._create_fallback_analysis(prompt)
            
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            
            # If OpenAI fails, return a basic analysis
            if "rate limit" in str(e).lower():
                raise  # Re-raise rate limit errors
            else:
                return self._create_fallback_analysis(prompt)
    
    def _validate_and_fix_analysis(self, analysis):
        """Validate and fix the analysis object with defaults"""
        defaults = {
            "primary_mood": "neutral",
            "secondary_moods": ["calm"],
            "emotions": ["relaxed"],
            "valence": "medium",
            "genre_suggestions": ["pop", "rock", "indie"],
            "subgenres": ["alternative"],
            "tempo": "medium",
            "energy_level": "medium",
            "danceability": "medium",
            "instrumentalness": "vocal",
            "acousticness": "mixed",
            "vocal_style": "melodic",
            "instruments": ["guitar", "piano"],
            "complexity": "moderate",
            "time_period": "2010s",
            "time_of_day": "any",
            "season": "any",
            "weather": "any",
            "activity": "general listening",
            "setting": "any",
            "themes": ["life", "love"],
            "lyrical_content": ["emotional"],
            "language": "english",
            "popularity": "mainstream"
        }
        
        # Fill in missing keys with defaults
        for key, default_value in defaults.items():
            if key not in analysis or not analysis[key]:
                analysis[key] = default_value
        
        return analysis
    
    def _create_fallback_analysis(self, prompt):
        """Create a basic analysis when OpenAI fails"""
        logging.warning("Using fallback analysis due to OpenAI failure")
        
        # Simple keyword-based analysis
        prompt_lower = prompt.lower()
        
        # Determine mood from keywords
        if any(word in prompt_lower for word in ["sad", "depressed", "down", "blue"]):
            primary_mood = "melancholy"
            valence = "low"
            energy_level = "low"
        elif any(word in prompt_lower for word in ["happy", "joy", "excited", "party"]):
            primary_mood = "upbeat"
            valence = "high"
            energy_level = "high"
        elif any(word in prompt_lower for word in ["chill", "relax", "calm", "peaceful"]):
            primary_mood = "relaxed"
            valence = "medium"
            energy_level = "low"
        else:
            primary_mood = "neutral"
            valence = "medium"
            energy_level = "medium"
        
        # Determine genres from keywords
        genres = ["pop", "rock"]
        if any(word in prompt_lower for word in ["hip hop", "rap", "hiphop"]):
            genres = ["hip-hop", "rap"]
        elif any(word in prompt_lower for word in ["rock", "metal", "punk"]):
            genres = ["rock", "alternative"]
        elif any(word in prompt_lower for word in ["jazz", "blues"]):
            genres = ["jazz", "blues"]
        elif any(word in prompt_lower for word in ["electronic", "edm", "dance"]):
            genres = ["electronic", "dance"]
        
        return {
            "primary_mood": primary_mood,
            "secondary_moods": ["nostalgic"],
            "emotions": ["contemplative"],
            "valence": valence,
            "genre_suggestions": genres,
            "subgenres": ["alternative"],
            "tempo": "medium",
            "energy_level": energy_level,
            "danceability": "medium",
            "instrumentalness": "vocal",
            "acousticness": "mixed",
            "vocal_style": "melodic",
            "instruments": ["guitar", "piano"],
            "complexity": "moderate",
            "time_period": "2010s",
            "time_of_day": "any",
            "season": "any",
            "weather": "any",
            "activity": "general listening",
            "setting": "any",
            "themes": ["life"],
            "lyrical_content": ["emotional"],
            "language": "english",
            "popularity": "mainstream"
        }
    
    def format_user_preferences(self, preferences):
        """Format user preferences for the AI prompt"""
        if not preferences:
            return ""
        
        formatted = []
        
        if preferences.get('favorite_artists'):
            formatted.append(f"Favorite Artists: {', '.join(preferences['favorite_artists'][:10])}")
        
        if preferences.get('favorite_genres'):
            formatted.append(f"Favorite Genres: {', '.join(preferences['favorite_genres'][:8])}")
        
        if preferences.get('recent_artists'):
            formatted.append(f"Recently Played Artists: {', '.join(preferences['recent_artists'][:5])}")
        
        if preferences.get('audio_preferences'):
            audio_prefs = preferences['audio_preferences']
            mood_desc = []
            if audio_prefs.get('prefers_positive_music'):
                mood_desc.append("upbeat/positive")
            if audio_prefs.get('prefers_high_energy'):
                mood_desc.append("high-energy")
            if audio_prefs.get('prefers_danceable'):
                mood_desc.append("danceable")
            if audio_prefs.get('prefers_acoustic'):
                mood_desc.append("acoustic")
            
            if mood_desc:
                formatted.append(f"Audio Preferences: {', '.join(mood_desc)}")
            
            formatted.append(f"Typical Tempo: ~{audio_prefs.get('average_tempo', 120)} BPM")
        
        return "\n".join(formatted)
    
    def format_user_preferences_for_context(self, preferences):
        """Format user preferences for AI context (not the song generation prompt)"""
        if not preferences:
            return ""
        
        formatted = []
        
        if preferences.get('favorite_artists'):
            formatted.append(f"Often listens to: {', '.join(preferences['favorite_artists'][:8])}")
        
        if preferences.get('favorite_genres'):
            formatted.append(f"Genre preferences: {', '.join(preferences['favorite_genres'][:6])}")
        
        if preferences.get('audio_preferences'):
            audio_prefs = preferences['audio_preferences']
            profile_desc = []
            
            valence = audio_prefs.get('valence_score', 0.5)
            energy = audio_prefs.get('energy_score', 0.5)
            
            if valence > 0.7:
                profile_desc.append("prefers upbeat/positive music")
            elif valence < 0.3:
                profile_desc.append("gravitates toward melancholic/introspective music")
            
            if energy > 0.7:
                profile_desc.append("enjoys high-energy tracks")
            elif energy < 0.3:
                profile_desc.append("prefers calmer, low-energy music")
            
            if audio_prefs.get('prefers_danceable'):
                profile_desc.append("likes danceable rhythms")
            
            if profile_desc:
                formatted.append(f"Musical tendencies: {', '.join(profile_desc)}")
        
        return "\n".join(formatted)