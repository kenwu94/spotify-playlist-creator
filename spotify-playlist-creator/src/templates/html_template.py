HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Spotify Playlist Creator</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --pastel-pink: #ffeef7;
            --pastel-lavender: #f0e6ff;
            --pastel-blue: #e6f2ff;
            --pastel-mint: #e6fff9;
            --pastel-peach: #ffe6d9;
            --pastel-yellow: #fff9e6;
            --soft-purple: #b19cd9;
            --soft-blue: #87ceeb;
            --soft-green: #98d8c8;
            --soft-coral: #f7a8a8;
            --soft-gray: #9ca3af;
            --dark-text: #374151;
            --medium-text: #6b7280;
            --light-text: #9ca3af;
            --white: #ffffff;
            --cream: #fefcf3;
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
            padding: 20px;
            color: var(--dark-text);
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container { 
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            padding: 50px;
            border-radius: 25px;
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
            z-index: 1;
        }
        
        h1 { 
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center; 
            margin-bottom: 15px;
            font-size: 2.5em;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        .subtitle { 
            text-align: center; 
            color: var(--medium-text); 
            margin-bottom: 40px; 
            font-size: 1.1em;
            font-weight: 400;
            line-height: 1.6;
        }
        
        .examples {
            background: rgba(255, 248, 230, 0.7);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 30px;
            border-radius: 20px;
            margin: 30px 0;
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
        }
        
        .examples h3 { 
            background: linear-gradient(135deg, var(--soft-coral), var(--soft-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
            font-size: 1.3em;
            font-weight: 600;
        }
        
        .example { 
            margin: 15px 0; 
            padding: 20px; 
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px; 
            border-left: 4px solid var(--soft-purple);
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 
                0 4px 15px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.7);
            transition: all 0.3s ease;
            line-height: 1.6;
        }
        
        .example:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .example strong {
            color: var(--soft-purple);
            font-weight: 600;
        }
        
        textarea { 
            width: 100%; 
            height: 160px; 
            padding: 25px; 
            margin: 20px 0; 
            border-radius: 20px; 
            border: 2px solid rgba(177, 156, 217, 0.3);
            font-size: 16px; 
            font-family: inherit;
            resize: vertical;
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            line-height: 1.6;
        }
        
        textarea:focus { 
            border-color: var(--soft-purple);
            outline: none;
            box-shadow: 0 0 0 4px rgba(177, 156, 217, 0.1);
            transform: translateY(-2px);
        }
        
        textarea::placeholder {
            color: var(--light-text);
            font-style: italic;
        }
        
        input[type="text"] { 
            width: 100%; 
            padding: 25px; 
            margin: 20px 0; 
            border-radius: 20px; 
            border: 2px solid rgba(177, 156, 217, 0.3);
            font-size: 16px;
            font-family: inherit;
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        input[type="text"]:focus { 
            border-color: var(--soft-purple);
            outline: none;
            box-shadow: 0 0 0 4px rgba(177, 156, 217, 0.1);
            transform: translateY(-2px);
        }
        
        input[type="text"]::placeholder {
            color: var(--light-text);
            font-style: italic;
        }
        
        button { 
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            color: white; 
            padding: 25px 50px; 
            border: none; 
            border-radius: 20px; 
            cursor: pointer; 
            font-size: 18px; 
            font-weight: 600; 
            width: 100%; 
            margin-top: 25px; 
            transition: all 0.3s ease;
            font-family: inherit;
            letter-spacing: 0.02em;
            box-shadow: 0 8px 25px rgba(177, 156, 217, 0.3);
        }
        
        button:hover { 
            background: linear-gradient(135deg, var(--soft-blue), var(--soft-green));
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(177, 156, 217, 0.4);
        }
        
        button:active {
            transform: translateY(-1px);
        }
        
        .result { 
            margin-top: 40px; 
            padding: 40px; 
            background: rgba(230, 242, 255, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 25px; 
            border-left: 6px solid var(--soft-blue);
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.4);
        }
        
        .result h3 {
            background: linear-gradient(135deg, var(--soft-blue), var(--soft-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 20px;
        }
        
        .result h4 {
            color: var(--soft-blue);
            font-weight: 600;
            margin: 25px 0 15px 0;
            font-size: 1.2em;
        }
        
        .loading { 
            display: none; 
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center; 
            font-size: 18px; 
            margin: 30px 0;
            font-weight: 500;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        .analysis-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
            gap: 25px; 
            margin: 30px 0; 
        }
        
        .analysis-card { 
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 25px; 
            border-radius: 20px; 
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.6);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .analysis-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
        }
        
        .result ul {
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 15px;
            margin-top: 20px;
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 
                0 4px 15px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
        }
        
        .result li {
            margin: 12px 0;
            padding: 10px 0;
            border-bottom: 1px solid rgba(177, 156, 217, 0.1);
            line-height: 1.6;
        }
        
        .result li:last-child {
            border-bottom: none;
        }
        
        .result a {
            color: var(--soft-blue);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .result a:hover {
            color: var(--soft-purple);
            text-decoration: underline;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                padding: 30px 25px;
                margin: 10px;
            }
            
            h1 {
                font-size: 2em;
            }
            
            .analysis-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            textarea, input[type="text"], button {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 AI Spotify Playlist Creator</h1>
        <p class="subtitle">The more detailed your description, the more personalized your playlist becomes!</p>
        
        <div class="examples">
            <h3>💡 Try these example prompts:</h3>
            <div class="example"><strong>Simple:</strong> "I get no hoes..."</div>
            <div class="example"><strong>Detailed:</strong> "I want to seem different from the others, so give me songs only from the 80s."</div>
            <div class="example"><strong>Very Detailed:</strong> "There are few people whom I really love, and still fewer of whom I think well. The more I see of the world, the more am I dissatisfied with it; and every day confirms my belief of the inconsistency of all human characters, and of the little dependence that can be placed on the appearance of merit or sense."</div>
        </div>
        
        <form id="playlistForm">
            <textarea id="prompt" placeholder="Describe your perfect playlist moment... The more details you provide (mood, setting, activity, time of day, weather, specific feelings, musical preferences), the more tailored your playlist will be!"></textarea>
            <input type="text" id="playlistName" placeholder="Playlist name (optional - AI will generate one based on your description)">
            <button type="submit">Create My Perfect Playlist ✨</button>
        </form>
        
        <div class="loading" id="loading">🎵 Analyzing your prompt and crafting the perfect playlist... This may take a moment.</div>
        <div id="result"></div>
    </div>

    <script>
        document.getElementById('playlistForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const prompt = document.getElementById('prompt').value;
            const playlistName = document.getElementById('playlistName').value;
            
            if (!prompt.trim()) {
                alert('Please enter a prompt!');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').innerHTML = '';
            
            try {
                const response = await fetch('/create-playlist', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt, playlist_name: playlistName })
                });
                
                const data = await response.json();
                document.getElementById('loading').style.display = 'none';
                
                if (data.error) {
                    document.getElementById('result').innerHTML = `<div style="color: red;">Error: ${data.error}</div>`;
                } else {
                    displayResult(data);
                }
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('result').innerHTML = `<div style="color: red;">Error: ${error.message}</div>`;
            }
        });
        
        function displayResult(data) {
            const analysis = data.analysis;
            const songs = data.songs;
            const playlist = data.playlist;
            
            const html = `
                <div class="result">
                    <h3>🎵 Playlist Created Successfully!</h3>
                    <p><strong>Name:</strong> ${playlist.name}</p>
                    <p><strong>Description:</strong> ${playlist.description}</p>
                    <p><strong>Detail Level:</strong> ${analysis.detail_level || 'basic'}</p>
                    <p><strong>Songs Found:</strong> ${songs.length}</p>
                    <p><strong>Playlist URL:</strong> <a href="${playlist.playlist_url}" target="_blank">${playlist.playlist_url}</a></p>
                    
                    <div class="analysis-grid">
                        <div class="analysis-card">
                            <h4>🎭 Mood & Emotion</h4>
                            <p><strong>Primary:</strong> ${analysis.primary_mood}</p>
                            ${analysis.secondary_moods ? `<p><strong>Secondary:</strong> ${analysis.secondary_moods.join(', ')}</p>` : ''}
                            <p><strong>Emotions:</strong> ${(analysis.emotions || []).map(e => `<span class="tag">${e}</span>`).join('')}</p>
                            <p><strong>Valence:</strong> ${analysis.valence}</p>
                        </div>
                        
                        <div class="analysis-card">
                            <h4>🎼 Musical Characteristics</h4>
                            <p><strong>Genres:</strong> ${analysis.genre_suggestions.map(g => `<span class="tag">${g}</span>`).join('')}</p>
                            ${analysis.subgenres ? `<p><strong>Subgenres:</strong> ${analysis.subgenres.map(s => `<span class="tag">${s}</span>`).join('')}</p>` : ''}
                            <p><strong>Tempo:</strong> ${analysis.tempo}</p>
                            <p><strong>Energy:</strong> ${analysis.energy_level}</p>
                            <p><strong>Danceability:</strong> ${analysis.danceability}</p>
                        </div>
                        
                        <div class="analysis-card">
                            <h4>🎤 Style & Production</h4>
                            <p><strong>Vocals:</strong> ${analysis.instrumentalness}</p>
                            <p><strong>Sound:</strong> ${analysis.acousticness}</p>
                            ${analysis.vocal_style ? `<p><strong>Vocal Style:</strong> ${analysis.vocal_style}</p>` : ''}
                            ${analysis.instruments ? `<p><strong>Instruments:</strong> ${analysis.instruments.map(i => `<span class="tag">${i}</span>`).join('')}</p>` : ''}
                            <p><strong>Complexity:</strong> ${analysis.complexity}</p>
                        </div>
                        
                        <div class="analysis-card">
                            <h4>🕐 Context & Setting</h4>
                            <p><strong>Time Period:</strong> ${analysis.time_period}</p>
                            ${analysis.time_of_day && analysis.time_of_day !== 'any' ? `<p><strong>Time of Day:</strong> ${analysis.time_of_day}</p>` : ''}
                            ${analysis.season && analysis.season !== 'any' ? `<p><strong>Season:</strong> ${analysis.season}</p>` : ''}
                            ${analysis.weather && analysis.weather !== 'any' ? `<p><strong>Weather:</strong> ${analysis.weather}</p>` : ''}
                            ${analysis.activity && analysis.activity !== 'general listening' ? `<p><strong>Activity:</strong> ${analysis.activity}</p>` : ''}
                            ${analysis.setting && analysis.setting !== 'any' ? `<p><strong>Setting:</strong> ${analysis.setting}</p>` : ''}
                        </div>
                        
                        <div class="analysis-card">
                            <h4>📝 Content & Themes</h4>
                            <p><strong>Themes:</strong> ${(analysis.themes || []).map(t => `<span class="tag">${t}</span>`).join('')}</p>
                            ${analysis.lyrical_content ? `<p><strong>Lyrical Content:</strong> ${analysis.lyrical_content.map(l => `<span class="tag">${l}</span>`).join('')}</p>` : ''}
                            <p><strong>Language:</strong> ${analysis.language || 'any'}</p>
                            <p><strong>Popularity:</strong> ${analysis.popularity}</p>
                        </div>
                    </div>
                    
                    <h4>🎵 Sample Songs (Placeholder):</h4>
                    <ul>
                        ${songs.slice(0, 8).map(song => `<li><strong>${song.name}</strong> by ${song.artist} <span class="tag">${song.genre}</span></li>`).join('')}
                        ${songs.length > 8 ? `<li><em>... and ${songs.length - 8} more songs</em></li>` : ''}
                    </ul>
                </div>
            `;
            document.getElementById('result').innerHTML = html;
        }
    </script>
</body>
</html>
"""