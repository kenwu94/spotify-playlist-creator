HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Spotify Playlist Creator</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --pastel-pink: #f5e6f0;
            --pastel-lavender: #e8ddf5;
            --pastel-blue: #ddeaf5;
            --pastel-mint: #ddf5f0;
            --pastel-peach: #f5e6d9;
            --pastel-yellow: #f5f0d9;
            --soft-purple: #a388c7;
            --soft-blue: #7bb8d9;
            --soft-green: #85c4b5;
            --soft-coral: #e89999;
            --soft-gray: #8a8a8a;
            --dark-text: #2d3748;
            --medium-text: #4a5568;
            --light-text: #718096;
            --white: #ffffff;
            --cream: #f7f5ed;
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
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            padding: 50px;
            border-radius: 25px;
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.25);
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
            text-align: center; 
            margin-bottom: 25px;
            font-size: 3.5em;
            font-weight: 900;
            letter-spacing: -0.04em;
            position: relative;
            padding: 20px 0;
            font-family: 'Times New Roman', Times, serif;
        }
        
        .dreamify-letter {
            display: inline-block;
            animation: letterFloat 3s ease-in-out infinite;
            background: linear-gradient(135deg, #d4a5c4, #c4a5d4, #a5c4d4, #a5d4c4, #d4c4a5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 2px 15px rgba(212, 165, 196, 0.5);
            transition: all 0.3s ease;
            font-family: 'Times New Roman', Times, serif;
        }
        
        .dreamify-letter:nth-child(2) { animation-delay: 0s; }
        .dreamify-letter:nth-child(3) { animation-delay: 0.1s; }
        .dreamify-letter:nth-child(4) { animation-delay: 0.2s; }
        .dreamify-letter:nth-child(5) { animation-delay: 0.3s; }
        .dreamify-letter:nth-child(6) { animation-delay: 0.4s; }
        .dreamify-letter:nth-child(7) { animation-delay: 0.5s; }
        .dreamify-letter:nth-child(8) { animation-delay: 0.6s; }
        .dreamify-letter:nth-child(9) { animation-delay: 0.7s; }
        .dreamify-letter:nth-child(10) { animation-delay: 0.8s; }
        
        .dreamify-letter:hover {
            transform: scale(1.2) rotate(5deg);
            text-shadow: 0 4px 25px rgba(212, 165, 196, 0.8);
        }
        
        @keyframes letterFloat {
            0%, 100% { 
                transform: translateY(0px) rotate(0deg);
                text-shadow: 0 2px 15px rgba(212, 165, 196, 0.5);
            }
            25% { 
                transform: translateY(-8px) rotate(2deg);
                text-shadow: 0 6px 20px rgba(196, 165, 212, 0.7);
            }
            50% { 
                transform: translateY(-12px) rotate(-1deg);
                text-shadow: 0 8px 25px rgba(165, 196, 212, 0.8);
            }
            75% { 
                transform: translateY(-6px) rotate(1deg);
                text-shadow: 0 6px 20px rgba(165, 212, 196, 0.7);
            }
        }
        
        .music-emoji {
            display: inline-block;
            animation: emojiSpin 4s ease-in-out infinite;
            margin-right: 15px;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1em;
            filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
        }
        
        @keyframes emojiSpin {
            0%, 100% { 
                transform: rotate(0deg) scale(1);
            }
            25% { 
                transform: rotate(-10deg) scale(1.1);
            }
            50% { 
                transform: rotate(0deg) scale(1.2);
            }
            75% { 
                transform: rotate(10deg) scale(1.1);
            }
        }
        
        h1::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 120%;
            height: 120%;
            background: radial-gradient(circle, rgba(212, 165, 196, 0.15) 0%, rgba(196, 165, 212, 0.15) 33%, rgba(165, 196, 212, 0.15) 66%, transparent 100%);
            border-radius: 50%;
            z-index: -1;
            animation: pastelHalo 4s ease-in-out infinite alternate;
        }
        
        @keyframes pastelHalo {
            0% { 
                transform: translate(-50%, -50%) scale(1);
                opacity: 0.3;
            }
            100% { 
                transform: translate(-50%, -50%) scale(1.1);
                opacity: 0.5;
            }
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
            background: rgba(247, 245, 237, 0.6);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 30px;
            border-radius: 20px;
            margin: 30px 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
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
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px; 
            border-left: 4px solid var(--soft-purple);
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 
                0 4px 15px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.6);
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
            border: 2px solid rgba(163, 136, 199, 0.4);
            font-size: 16px; 
            font-family: inherit;
            resize: vertical;
            background: rgba(255, 255, 255, 0.6);
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
            border: 2px solid rgba(163, 136, 199, 0.4);
            font-size: 16px;
            font-family: inherit;
            background: rgba(255, 255, 255, 0.6);
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
        
        input[type="number"] { 
            width: 100%; 
            padding: 15px; 
            margin: 8px 0 20px 0; 
            border-radius: 15px; 
            border: 2px solid rgba(163, 136, 199, 0.4);
            font-size: 16px;
            font-family: inherit;
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        input[type="number"]:focus { 
            border-color: var(--soft-purple);
            outline: none;
            box-shadow: 0 0 0 4px rgba(177, 156, 217, 0.1);
            transform: translateY(-2px);
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
            background: rgba(221, 234, 245, 0.5);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 25px; 
            border-left: 6px solid var(--soft-blue);
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.12),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.3);
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
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 25px; 
            border-radius: 20px; 
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
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
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 15px;
            margin-top: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 
                0 4px 15px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
        }
        
        .result li {
            margin: 12px 0;
            padding: 10px 0;
            border-bottom: 1px solid rgba(163, 136, 199, 0.15);
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
        
        .auth-section {
            text-align: center;
            margin: 40px 0;
        }
        
        .login-prompt {
            background: rgba(247, 245, 237, 0.6);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
        }
        
        .login-prompt h3 {
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            font-size: 1.3em;
            font-weight: 600;
        }
        
        .login-prompt p {
            color: var(--medium-text);
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .spotify-btn {
            background: linear-gradient(135deg, #1DB954, #1ed760);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
            display: inline-block;
            margin: 10px 0;
            box-shadow: 0 8px 25px rgba(29, 185, 84, 0.3);
        }
        
        .spotify-btn:hover {
            background: linear-gradient(135deg, #1ed760, #1fdf64);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(29, 185, 84, 0.4);
        }
        
        .user-info {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }
        
        .user-info span {
            margin: 10px 0;
            font-size: 18px;
            font-weight: 500;
            color: var(--dark-text);
        }
        
        .logout-btn {
            background: transparent;
            color: var(--soft-purple);
            border: 2px solid var(--soft-purple);
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .logout-btn:hover {
            background: var(--soft-purple);
            color: white;
        }
        
        /* Custom Slider Styles */
        .slider-wrapper {
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            margin-top: 10px;
        }
        
        .slider-min, .slider-max {
            font-size: 14px;
            color: var(--medium-text);
        }
        
        .custom-slider {
            -webkit-appearance: none;
            appearance: none;
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: rgba(163, 136, 199, 0.3);
            position: relative;
            cursor: pointer;
        }
        
        .custom-slider .slider-track {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            border-radius: 5px;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            z-index: 1;
        }
        
        .custom-slider .slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: white;
            border: 2px solid var(--soft-purple);
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(45deg);
            width: 20px;
            height: 20px;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            border: 3px solid white;
            border-radius: 4px;
            pointer-events: none;
            z-index: 3;
            transition: left 0.2s ease, transform 0.15s ease;
            box-shadow: 
                0 3px 12px rgba(163, 136, 199, 0.4),
                inset 0 1px 3px rgba(255, 255, 255, 0.6);
        }
        
        .custom-slider .slider-thumb::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 8px;
            height: 8px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 2px;
            box-shadow: 0 0 6px rgba(255, 255, 255, 0.8);
        }
        
        /* Minimalist Song Count Slider */
        .song-count-container {
            background: transparent;
            padding: 15px 0;
            border: none;
            transition: all 0.3s ease;
        }
        
        .slider-label {
            display: block;
            margin-bottom: 12px;
            font-weight: 500;
            color: var(--medium-text);
            text-align: center;
            font-size: 1em;
            font-family: inherit;
        }
        
        #songCountValue {
            color: var(--soft-purple);
            font-weight: 600;
        }
        
        .slider-wrapper {
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
        }
        
        .slider-min, .slider-max {
            font-weight: 500;
            color: var(--light-text);
            font-size: 0.85em;
            min-width: 20px;
            text-align: center;
        }
        
        .custom-slider {
            flex: 1;
            position: relative;
            height: 24px;
            display: flex;
            align-items: center;
        }
        
        .slider {
            width: 100%;
            height: 4px;
            border-radius: 2px;
            background: rgba(163, 136, 199, 0.2);
            outline: none;
            transition: all 0.2s ease;
            -webkit-appearance: none;
            appearance: none;
            cursor: pointer;
            position: relative;
            z-index: 2;
        }
        
        .slider:hover {
            background: rgba(163, 136, 199, 0.3);
        }
        
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 0;
            height: 0;
            background: transparent;
            border: none;
            cursor: pointer;
        }
        
        .slider::-moz-range-thumb {
            width: 0;
            height: 0;
            background: transparent;
            border: none;
            cursor: pointer;
            -moz-appearance: none;
        }
        
        .slider::-ms-thumb {
            width: 0;
            height: 0;
            background: transparent;
            border: none;
            cursor: pointer;
        }
        
        .slider-thumb {
            position: absolute;
            top: 50%;
            left: 37.5%; /* This will be overridden by JavaScript */
            transform: translate(-50%, -50%) rotate(45deg);
            width: 20px;
            height: 20px;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            border: 3px solid white;
            border-radius: 4px;
            pointer-events: none;
            z-index: 3;
            transition: left 0.2s ease, transform 0.15s ease;
            box-shadow: 
                0 3px 12px rgba(163, 136, 199, 0.4),
                inset 0 1px 3px rgba(255, 255, 255, 0.6);
        }
        
        .slider-thumb::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 8px;
            height: 8px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 2px;
            box-shadow: 0 0 6px rgba(255, 255, 255, 0.8);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .slider-wrapper {
                gap: 8px;
            }
            
            .slider::-webkit-slider-thumb {
                width: 18px;
                height: 18px;
            }
            
            .slider::-moz-range-thumb {
                width: 18px;
                height: 18px;
            }
            
            .slider-thumb {
                width: 16px;
                height: 16px;
            }
            
            .slider-thumb::before {
                width: 6px;
                height: 6px;
            }
        }
        
        .playlist-header {
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            background: linear-gradient(135deg, rgba(163, 136, 199, 0.1), rgba(123, 184, 217, 0.1));
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .success-icon {
            font-size: 3em;
            margin-bottom: 15px;
            animation: bounce 2s ease-in-out infinite;
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        
        .success-title {
            background: linear-gradient(135deg, var(--soft-blue), var(--soft-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.8em;
            font-weight: 700;
            margin-bottom: 15px;
        }
        
        .playlist-name {
            font-size: 1.4em;
            font-weight: 600;
            color: var(--soft-purple);
            font-style: italic;
            margin-bottom: 10px;
        }
        
        .playlist-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .detail-card, .playlist-link-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
        }
        
        .detail-card:hover, .playlist-link-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
        }
        
        .detail-icon, .link-icon {
            font-size: 1.8em;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            min-width: 40px;
        }
        
        .detail-content, .link-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .detail-label, .link-label {
            font-size: 0.9em;
            color: var(--light-text);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .detail-value {
            font-size: 1.1em;
            color: var(--dark-text);
            font-weight: 600;
        }
        
        .spotify-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(163, 136, 199, 0.3);
        }
        
        .spotify-link:hover {
            background: linear-gradient(135deg, #1ed760, #1fdf64);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(163, 136, 199, 0.4);
            color: white;
            text-decoration: none;
        }
        
        .external-icon {
            font-size: 0.8em;
            opacity: 0.8;
        }
        
        .tag {
            display: inline-block;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 500;
            margin: 2px 4px 2px 0;
            box-shadow: 0 2px 8px rgba(163, 136, 199, 0.3);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .playlist-details {
                grid-template-columns: 1fr;
                gap: 15px;
            }
            
            .playlist-header {
                padding: 20px;
            }
            
            .success-icon {
                font-size: 2.5em;
            }
            
            .success-title {
                font-size: 1.5em;
            }
            
            .playlist-name {
                font-size: 1.2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>
            <span class="music-emoji">🎵</span>
            <span class="dreamify-letter">D</span>
            <span class="dreamify-letter">r</span>
            <span class="dreamify-letter">e</span>
            <span class="dreamify-letter">a</span>
            <span class="dreamify-letter">m</span>
            <span class="dreamify-letter">i</span>
            <span class="dreamify-letter">f</span>
            <span class="dreamify-letter">y</span>
        </h1>
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
            
            <!-- Minimalist Song Count Slider -->
            <div class="song-count-container" style="margin: 20px 0;">
                <label for="songCount" class="slider-label">Songs: <span id="songCountValue">25</span></label>
                <div class="slider-wrapper">
                    <span class="slider-min">10</span>
                    <div class="custom-slider">
                        <input type="range" id="songCount" min="10" max="50" value="25" class="slider">
                        <div class="slider-thumb"></div>
                    </div>
                    <span class="slider-max">50</span>
                </div>
            </div>
            
            <button type="submit">Make My Playlist ⭐</button>
        </form>
        
        <div class="loading" id="loading">🎵 Analyzing your prompt and crafting the perfect playlist... This may take a moment.</div>
        <div id="result"></div>
        
        <!-- Authentication sections -->
        <div id="login-section" class="auth-section" style="display: none;">
            <div class="login-prompt">
                <h3>🌙 Transform Dreams into Playlists</h3>
                <p>Share a dream, quote, mood, or moment from your life, and watch as we craft a personalized playlist that captures its essence. Every emotion deserves its soundtrack—let's create yours.</p>
                <p style="font-style: italic; color: var(--light-text); margin-top: 15px;">Connect with Spotify to bring your musical visions to life and save them to your library.</p>
                <button onclick="loginToSpotify()" class="spotify-btn">
                    ✨ Connect & Create
                </button>
            </div>
        </div>
        
        <div id="user-section" class="auth-section" style="display: none;">
            <div class="user-info">
                <img id="user-avatar" src="" alt="User" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;">
                <span id="user-name" style="margin-right: 15px;"></span>
                <button onclick="logout()" class="logout-btn">Logout</button>
            </div>
        </div>
    </div>

    <script>
        // Song count slider functionality
        const songSlider = document.getElementById('songCount');
        const songCountValue = document.getElementById('songCountValue');
        const sliderThumb = document.querySelector('.slider-thumb');
        
        function updateSlider() {
            const value = songSlider.value;
            songCountValue.textContent = value;
            
            // Calculate position for slider thumb (0% to 100%)
            const percentage = ((value - 10) / (50 - 10)) * 100;
            sliderThumb.style.left = `${percentage}%`;
            
            // Add a subtle scale animation
            sliderThumb.style.transform = 'translate(-50%, -50%) rotate(45deg) scale(1.15)';
            setTimeout(() => {
                sliderThumb.style.transform = 'translate(-50%, -50%) rotate(45deg) scale(1)';
            }, 150);
        }
        
        // Add mouse event listeners for better responsiveness
        songSlider.addEventListener('input', updateSlider);
        songSlider.addEventListener('change', updateSlider);
        songSlider.addEventListener('mousemove', updateSlider);
        
        // Initialize slider position
        updateSlider();
        
        document.getElementById('playlistForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const prompt = document.getElementById('prompt').value;
            const playlistName = document.getElementById('playlistName').value;
            const songCount = parseInt(document.getElementById('songCount').value) || 25;
            
            // Validate song count
            if (songCount < 10 || songCount > 50) {
                alert('Please select a number between 10 and 50 songs');
                return;
            }
            
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
                    body: JSON.stringify({ 
                        prompt, 
                        playlist_name: playlistName,
                        song_count: songCount 
                    })
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
                    <div class="playlist-header">
                        <div class="success-icon">🎵</div>
                        <h3 class="success-title">Playlist Created Successfully!</h3>
                        <div class="playlist-name">"${playlist.name}"</div>
                    </div>
                    
                    <div class="playlist-details">
                        <div class="detail-card">
                            <div class="detail-icon">📝</div>
                            <div class="detail-content">
                                <span class="detail-label">Description</span>
                                <span class="detail-value">${playlist.description}</span>
                            </div>
                        </div>
                        
                        <div class="detail-card">
                            <div class="detail-icon">🎶</div>
                            <div class="detail-content">
                                <span class="detail-label">Songs Found</span>
                                <span class="detail-value">${songs.length} tracks</span>
                            </div>
                        </div>
                        
                        <div class="detail-card">
                            <div class="detail-icon">📊</div>
                            <div class="detail-content">
                                <span class="detail-label">Analysis Level</span>
                                <span class="detail-value">${analysis.detail_level || 'basic'}</span>
                            </div>
                        </div>
                        
                        <div class="playlist-link-card">
                            <div class="link-icon">🎧</div>
                            <div class="link-content">
                                <span class="link-label">Listen on Spotify</span>
                                <a href="${playlist.playlist_url}" target="_blank" class="spotify-link">
                                    Open Playlist
                                    <span class="external-icon">↗</span>
                                </a>
                            </div>
                        </div>
                    </div>
                    
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
                    
                    <h4>🎵 Sample Songs:</h4>
                    <ul>
                        ${songs.slice(0, 8).map(song => `<li><strong>${song.name}</strong> by ${song.artist} <span class="tag">${song.genre}</span></li>`).join('')}
                        ${songs.length > 8 ? `<li><em>... and ${songs.length - 8} more songs</em></li>` : ''}
                    </ul>
                </div>
            `;
            document.getElementById('result').innerHTML = html;
        }
        
        // Check authentication status on page load
        window.onload = function() {
            checkAuthStatus();
        };

        function checkAuthStatus() {
            fetch('/auth/user-info')
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Not authenticated');
                    }
                })
                .then(user => {
                    showUserSection(user);
                })
                .catch(() => {
                    showLoginSection();
                });
        }

        function showLoginSection() {
            document.getElementById('login-section').style.display = 'block';
            document.getElementById('user-section').style.display = 'none';
            
            // Disable the form
            document.getElementById('playlistForm').style.opacity = '0.5';
            document.getElementById('playlistForm').style.pointerEvents = 'none';
        }

        function showUserSection(user) {
            document.getElementById('login-section').style.display = 'none';
            document.getElementById('user-section').style.display = 'block';
            
            // Enable the form
            document.getElementById('playlistForm').style.opacity = '1';
            document.getElementById('playlistForm').style.pointerEvents = 'auto';
            
            document.getElementById('user-name').textContent = user.display_name;
            if (user.images && user.images.length > 0) {
                document.getElementById('user-avatar').src = user.images[0].url;
            }
        }

        function loginToSpotify() {
            window.location.href = '/auth/login';
        }

        function logout() {
            window.location.href = '/auth/logout';
        }

        async function createPlaylist() {
            // Check if user is authenticated
            const authResponse = await fetch('/auth/user-info');
            if (!authResponse.ok) {
                alert('Please login to Spotify first to create playlists!');
                return;
            }
            
            // ...rest of playlist creation code...
        }
    </script>
</body>
</html>
"""