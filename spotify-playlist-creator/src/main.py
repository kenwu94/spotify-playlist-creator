import os
import sys
from flask import Flask, render_template_string
from dotenv import load_dotenv

# Add the src directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.playlist_routes import playlist_bp
from templates.html_template import HTML_TEMPLATE

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Register blueprints
app.register_blueprint(playlist_bp)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("🎵 Starting Enhanced AI Spotify Playlist Creator...")
    print("🎵 Make sure to set your OPENAI_API_KEY in a .env file")
    print("🎵 Now with modular architecture!")
    print("🎵 Spotify API integration is placeholder for now")
    app.run(debug=True, port=5000)