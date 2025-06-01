HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Spotify Playlist Creator</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f8f9fa; }
        .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { color: #1db954; text-align: center; margin-bottom: 10px; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; font-style: italic; }
        textarea { width: 100%; height: 140px; padding: 20px; margin: 15px 0; border-radius: 10px; border: 2px solid #e0e0e0; font-size: 16px; resize: vertical; }
        textarea:focus { border-color: #1db954; outline: none; }
        input[type="text"] { width: 100%; padding: 20px; margin: 15px 0; border-radius: 10px; border: 2px solid #e0e0e0; font-size: 16px; }
        input[type="text"]:focus { border-color: #1db954; outline: none; }
        button { background: linear-gradient(135deg, #1db954, #1ed760); color: white; padding: 20px 40px; border: none; border-radius: 10px; cursor: pointer; font-size: 18px; font-weight: bold; width: 100%; margin-top: 20px; transition: all 0.3s; }
        button:hover { background: linear-gradient(135deg, #1ed760, #1db954); transform: translateY(-2px); }
        .result { margin-top: 30px; padding: 30px; background: #f8f9fa; border-radius: 10px; border-left: 5px solid #1db954; }
        .loading { display: none; color: #1db954; text-align: center; font-size: 18px; margin: 20px 0; }
        .analysis-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .analysis-card { background: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; }
        .analysis-card h4 { color: #1db954; margin-top: 0; }
        .tag { display: inline-block; background: #1db954; color: white; padding: 5px 10px; border-radius: 15px; margin: 2px; font-size: 12px; }
        .examples { background: #f0f8ff; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .examples h3 { color: #1db954; margin-top: 0; }
        .example { margin: 10px 0; padding: 10px; background: white; border-radius: 5px; border-left: 3px solid #1db954; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 AI Spotify Playlist Creator</h1>
        <p class="subtitle">The more detailed your description, the more personalized your playlist becomes!</p>
        
        <div class="examples">
            <h3>💡 Try these example prompts:</h3>
            <div class="example"><strong>Simple:</strong> "Happy morning vibes"</div>
            <div class="example"><strong>Detailed:</strong> "I'm driving through the countryside on a foggy autumn morning, feeling nostalgic about old friendships. I want acoustic guitar-driven songs from the 2000s with thoughtful lyrics."</div>
            <div class="example"><strong>Very Detailed:</strong> "Picture this: It's 2 AM, I'm in my dimly lit apartment, rain pattering against the windows. I just finished reading a melancholic novel about lost love. I want to hear slow, atmospheric music with ethereal female vocals, maybe some trip-hop or ambient electronic elements, songs that feel like they belong in a David Lynch film."</div>
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