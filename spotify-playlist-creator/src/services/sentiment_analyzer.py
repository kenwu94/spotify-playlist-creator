import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def analyze_prompt(self, user_prompt):
        """Analyze user input and extract detailed musical sentiments and characteristics"""
        system_prompt = """
        You are an expert music curator AI. Analyze the given text and extract detailed musical characteristics that would make a perfect playlist. The more detailed the user's input, the more specific and nuanced your analysis should be.

        Return a JSON object with the following structure (include ALL fields, but make them more detailed/specific based on input complexity):
        {
            "primary_mood": "string (main emotional tone)",
            "secondary_moods": ["mood2", "mood3"] (supporting emotions if input is detailed),
            "genre_suggestions": ["genre1", "genre2", "genre3"] (3-6 genres based on input detail),
            "subgenres": ["subgenre1", "subgenre2"] (specific subgenres if input warrants it),
            "tempo": "string (very slow, slow, medium-slow, medium, medium-fast, fast, very fast)",
            "energy_level": "string (very low, low, medium-low, medium, medium-high, high, very high)",
            "danceability": "string (not danceable, slightly danceable, moderately danceable, very danceable)",
            "valence": "string (very sad, sad, neutral, happy, very happy)",
            "instrumentalness": "string (vocals preferred, mixed, instrumental preferred)",
            "acousticness": "string (electronic, mixed, acoustic)",
            "themes": ["theme1", "theme2", "theme3"] (expand based on input detail),
            "emotions": ["emotion1", "emotion2"] (specific emotions beyond mood),
            "time_period": "string (specific decade or era)",
            "time_of_day": "string (morning, afternoon, evening, night, late night) if applicable",
            "season": "string (spring, summer, fall, winter) if applicable",
            "activity": "string (studying, working out, driving, relaxing, etc.) if applicable",
            "setting": "string (home, car, party, nature, etc.) if applicable",
            "weather": "string (sunny, rainy, cloudy, snowy, etc.) if applicable",
            "lyrical_content": ["content_type1", "content_type2"] (love, heartbreak, motivation, etc.),
            "vocal_style": "string (soft, powerful, raspy, smooth, etc.) if specified",
            "instruments": ["instrument1", "instrument2"] (if specific instruments mentioned),
            "complexity": "string (simple, moderate, complex) - musical complexity",
            "popularity": "string (mainstream, alternative, underground) preference",
            "language": "string (english, spanish, any, etc.) if specified,
            "playlist_description": "string (detailed description based on analysis)",
            "song_count": "number (10-50 based on scope of request)",
            "detail_level": "string (basic, moderate, detailed, very detailed) - based on input complexity"
        }

        Guidelines:
        - For simple inputs (1-2 sentences): Focus on basic mood, genre, energy
        - For moderate inputs (paragraph): Add time/setting context, more specific themes
        - For detailed inputs (multiple paragraphs/very specific): Include all nuanced characteristics
        - Extract specific details mentioned (instruments, artists, time periods, activities)
        - If user mentions specific songs/artists, factor their style into genre/mood analysis
        - Be creative but accurate in interpreting abstract concepts into musical characteristics
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this for creating a music playlist (be proportionally detailed): {user_prompt}"}
                ],
                temperature=0.8
            )
            
            # Parse the JSON response
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            print(f"Error analyzing prompt: {e}")
            return self.get_default_analysis()
    
    def get_default_analysis(self):
        """Return default analysis if OpenAI call fails"""
        return {
            "primary_mood": "chill",
            "secondary_moods": ["relaxed"],
            "genre_suggestions": ["pop", "indie", "alternative"],
            "subgenres": ["indie pop"],
            "tempo": "medium",
            "energy_level": "medium",
            "danceability": "moderately danceable",
            "valence": "neutral",
            "instrumentalness": "vocals preferred",
            "acousticness": "mixed",
            "themes": ["general", "mood"],
            "emotions": ["calm", "content"],
            "time_period": "modern",
            "time_of_day": "any",
            "season": "any",
            "activity": "general listening",
            "setting": "any",
            "weather": "any",
            "lyrical_content": ["general"],
            "vocal_style": "smooth",
            "instruments": ["guitar", "drums"],
            "complexity": "moderate",
            "popularity": "mainstream",
            "language": "english",
            "playlist_description": "A curated playlist based on your prompt",
            "song_count": 15,
            "detail_level": "basic"
        }