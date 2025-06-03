LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dreamify - Login to Spotify</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --pastel-pink: #f5e6f0;
            --pastel-lavender: #e8ddf5;
            --pastel-blue: #ddeaf5;
            --pastel-mint: #ddf5f0;
            --pastel-peach: #f5e6d9;
            --soft-purple: #a388c7;
            --soft-blue: #7bb8d9;
            --soft-green: #85c4b5;
            --dark-text: #2d3748;
            --medium-text: #4a5568;
            --light-text: #718096;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: linear-gradient(135deg, var(--pastel-pink) 0%, var(--pastel-lavender) 25%, var(--pastel-blue) 50%, var(--pastel-mint) 75%, var(--pastel-peach) 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            color: var(--dark-text);
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .login-container { 
            max-width: 500px;
            width: 100%;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            padding: 60px 40px;
            border-radius: 25px;
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.25);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .login-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
            z-index: 1;
        }
        
        .logo { 
            font-size: 3.5em;
            font-weight: 900;
            letter-spacing: -0.04em;
            margin-bottom: 20px;
            font-family: 'Times New Roman', Times, serif;
            background: linear-gradient(135deg, #d4a5c4, #c4a5d4, #a5c4d4, #a5d4c4, #d4c4a5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .logo::before {
            content: '🎵';
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
            margin-right: 10px;
        }
        
        .welcome-text {
            font-size: 1.3em;
            color: var(--medium-text);
            margin-bottom: 15px;
            font-weight: 500;
        }
        
        .description {
            font-size: 1em;
            color: var(--light-text);
            margin-bottom: 40px;
            line-height: 1.6;
        }
        
        .features {
            background: rgba(247, 245, 237, 0.6);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 25px;
            border-radius: 20px;
            margin: 30px 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
            text-align: left;
        }
        
        .features h3 {
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            font-size: 1.2em;
            font-weight: 600;
            text-align: center;
        }

        .features h3::before {
            content: '✨';
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
            margin-right: 8px;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            margin: 12px 0;
            padding: 8px 0;
        }
        
        .feature-icon {
            font-size: 1.5em;
            margin-right: 15px;
            min-width: 30px;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue), var(--soft-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
        }
        
        .spotify-login-btn {
            background: linear-gradient(135deg, #1DB954, #1ed760);
            color: white;
            padding: 20px 40px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            width: 100%;
            margin-top: 30px;
            transition: all 0.3s ease;
            font-family: inherit;
            letter-spacing: 0.02em;
            box-shadow: 0 8px 25px rgba(29, 185, 84, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }
        
        .spotify-login-btn:hover {
            background: linear-gradient(135deg, #1ed760, #1fdf64);
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(29, 185, 84, 0.4);
        }
        
        .spotify-login-btn:active {
            transform: translateY(-1px);
        }
        
        .spotify-icon {
            width: 24px;
            height: 24px;
            filter: brightness(0) invert(1);
        }
        
        .security-note {
            margin-top: 25px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 15px;
            font-size: 0.9em;
            color: var(--light-text);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .security-note strong {
            color: var(--medium-text);
        }

        .security-note strong::before {
            content: '🔒';
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
            margin-right: 6px;
        }
          /* Responsive design */
        @media (max-width: 768px) {
            body {
                min-height: 100vh;
                padding: 10px;
            }
            
            .login-container {
                padding: 30px 20px;
                margin: 10px 0;
                min-height: calc(100vh - 40px);
                width: 100%;
                max-width: none;
            }
            
            .logo {
                font-size: 2.2em;
                margin-bottom: 15px;
            }
            
            .welcome-text {
                font-size: 1.0em;
                line-height: 1.5;
                margin-bottom: 25px;
            }
        
            .login-btn {
                padding: 18px 35px;
                font-size: 16px;
                width: 100%;
                max-width: 280px;
            }
            
            .security-note {
                font-size: 0.85em;
                line-height: 1.4;
                margin-top: 25px;
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">Dreamify</div>
        <div class="welcome-text">Transform Dreams into Playlists</div>
        <div class="description">
            Share a dream, quote, mood, or moment from your life, and watch as we craft a personalized playlist that captures its essence. Every emotion deserves its soundtrack—let's create yours.
        </div>
        
        <div class="features">
            <h3>What You'll Get</h3>
            <div class="feature-item">
                <span class="feature-icon">🌙</span>
                <span>Turn dreams and emotions into music</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🎭</span>
                <span>AI-powered mood interpretation</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🎨</span>
                <span>Aesthetic-driven song curation</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">✨</span>
                <span>Instant Spotify playlist creation</span>
            </div>
        </div>
        
        <button onclick="loginToSpotify()" class="spotify-login-btn">
            <img src="/static/spotify_logo.png" alt="Spotify" class="spotify-icon">
            Login With Spotify
        </button>
        
        <div class="security-note">
            <strong>Secure:</strong> We only access your public profile and playlist creation permissions. Your musical visions remain private.
        </div>
    </div>

    <script>
        function loginToSpotify() {
            window.location.href = '/auth/login';
        }    </script>
    
    <!-- Footer with legal links -->
    <footer style="position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); text-align: center; color: var(--light-text); font-size: 0.85em;">
        <div>
            <a href="/privacy-policy" style="color: var(--medium-text); text-decoration: none; margin: 0 15px;" target="_blank">Privacy Policy</a>
            <a href="/terms-of-service" style="color: var(--medium-text); text-decoration: none; margin: 0 15px;" target="_blank">Terms of Service</a>
        </div>
    </footer>
</body>
</html>
"""