HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
            background-size: 200% 200%; /* Reduced from 400% */
            animation: gradientShift 30s ease infinite; /* Slowed down from 15s */
            min-height: 100vh;
            padding: 20px;
            color: var(--dark-text);
        }
        
        /* Optimize the main background gradient - reduce frequency */
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container { 
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.85); /* Increased opacity */
            backdrop-filter: blur(10px); /* Reduced from 25px */
            -webkit-backdrop-filter: blur(10px);
            padding: 50px;
            border-radius: 25px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15),
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
            animation: letterFloat 4s ease-in-out infinite; /* Slowed down */
            background: linear-gradient(135deg, #d4a5c4, #c4a5d4, #a5c4d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            will-change: transform; /* Optimize for animations */
            transition: all 0.3s ease;
            font-family: 'Times New Roman', Times, serif;
        }
        
        /* Optimize letter animations - use transform only */
        @keyframes letterFloat {
            0%, 100% { 
                transform: translateY(0px);
            }
            25% { 
                transform: translateY(-4px); /* Reduced movement */
            }
            50% { 
                transform: translateY(-8px); /* Reduced movement */
            }
            75% { 
                transform: translateY(-2px); /* Reduced movement */
            }
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
            position: relative;
        }
        
        .spotify-btn::before {
            content: '✨';
            background: linear-gradient(135deg, #1DB954, #1ed760);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 2px 4px rgba(29, 185, 84, 0.3));
            margin-right: 8px;
        }
        
        button:hover { 
            background: linear-gradient(135deg, var(--soft-blue), var(--soft-green));
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(177, 156, 217, 0.4);
        }
        
        button:active {
            transform: translateY(-1px);
        }
        
        button:disabled {
            background: linear-gradient(135deg, var(--soft-gray), var(--light-text));
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
            opacity: 0.6;
        }
        
        button:disabled:hover {
            background: linear-gradient(135deg, var(--soft-gray), var(--light-text));
            transform: none;
            box-shadow: none;
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
            background: linear-gradient(135deg, var(--soft-blue), var(--soft-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
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
          /* Cool Loading Animation */
        .playlist-generator {
            display: none;
            text-align: center;
            margin: 40px auto;
            padding: 40px;
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.12),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
            position: relative;
            overflow: hidden;
            max-width: 600px;
            width: 90%;
        }
        
        .playlist-generator::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(163, 136, 199, 0.05), transparent);
            animation: shimmer 3s ease-in-out infinite;
            transform: rotate(45deg);
        }
        
        @keyframes shimmer {
            0%, 100% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            50% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .floating-notes {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .note {
            position: absolute;
            font-size: 1.2em; /* Reduced size */
            opacity: 0.2; /* Reduced default opacity */
            animation: floatNote 6s ease-in-out infinite; /* Slowed down */
            color: var(--soft-purple);
            will-change: transform, opacity;
        }
        
        /* Simplify floating notes */
        @keyframes floatNote {
            0%, 100% { 
                transform: translateY(60px);
                opacity: 0;
            }
            50% { 
                transform: translateY(-10px);
                opacity: 0.4; /* Reduced opacity */
            }
        }
        
        .vinyl-record {
            position: absolute;
            top: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            box-shadow: 
                0 2px 8px rgba(163, 136, 199, 0.3),
                inset 0 0 0 4px rgba(255, 255, 255, 0.2),
                inset 0 0 0 6px var(--soft-purple),
                inset 0 0 0 8px rgba(255, 255, 255, 0.3);
            animation: vinylSpin 8s linear infinite; /* Slowed down from 4s */
            z-index: 2;
            opacity: 0.7;
        }
        
        /* Optimize vinyl record animation */
        @keyframes vinylSpin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .vinyl-record::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 4px;
            height: 4px;
            background: linear-gradient(135deg, var(--soft-blue), var(--soft-green));
            border-radius: 50%;
            box-shadow: 0 0 4px rgba(163, 136, 199, 0.4);
        }
        
        .vinyl-record::after {
            content: '♪';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 0.8em;
            color: white;
            text-shadow: 0 0 6px rgba(255, 255, 255, 0.6);
            animation: noteFloat 2s ease-in-out infinite alternate;
        }
        
        @keyframes noteFloat {
            0% { transform: translate(-50%, -50%) scale(1); }
            100% { transform: translate(-50%, -50%) scale(1.1); }
        }
        
        .music-visualizer {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            height: 100px;
            margin: 30px 0;
            gap: 8px;
            position: relative;
            z-index: 2;
        }
        
        .bar {
            width: 6px;
            background: linear-gradient(to top, var(--soft-purple), var(--soft-blue));
            border-radius: 3px;
            animation: musicBars 2s ease-in-out infinite; /* Slowed down */
            transform-origin: bottom;
            will-change: transform; /* Optimize for animations */
            box-shadow: 0 0 10px rgba(163, 136, 199, 0.4);
        }
        
        /* Optimize music bars - use scale instead of height changes */
        @keyframes musicBars {
            0%, 100% { 
                transform: scaleY(0.3);
                opacity: 0.6;
            }
            50% { 
                transform: scaleY(1);
                opacity: 1;
            }
        }
        
        .bar:nth-child(1) { animation-delay: 0s; height: 25px; }
        .bar:nth-child(2) { animation-delay: 0.1s; height: 40px; }
        .bar:nth-child(3) { animation-delay: 0.2s; height: 60px; }
        .bar:nth-child(4) { animation-delay: 0.3s; height: 80px; }
        .bar:nth-child(5) { animation-delay: 0.4s; height: 55px; }
        .bar:nth-child(6) { animation-delay: 0.5s; height: 70px; }
        .bar:nth-child(7) { animation-delay: 0.6s; height: 35px; }
        .bar:nth-child(8) { animation-delay: 0.7s; height: 65px; }
        .bar:nth-child(9) { animation-delay: 0.8s; height: 45px; }
        .bar:nth-child(10) { animation-delay: 0.9s; height: 30px; }
        .bar:nth-child(11) { animation-delay: 1.0s; height: 50px; }
        .bar:nth-child(12) { animation-delay: 1.1s; height: 40px; }
        
        .loading-text {
            font-size: 1.6em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue), var(--soft-green));
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
            animation: textFlow 3s ease-in-out infinite;
            position: relative;
            z-index: 2;
            text-shadow: 0 0 30px rgba(163, 136, 199, 0.3);
        }
        
        @keyframes textFlow {
            0%, 100% { 
                background-position: 0% 50%;
                transform: scale(1);
            }
            50% { 
                background-position: 100% 50%;
                transform: scale(1.05);
            }
        }
        
        .loading-steps {
            list-style: none;
            padding: 0;
            margin: 30px 0;
            position: relative;
            z-index: 2;
        }
        
        .loading-step {
            padding: 15px 20px;
            margin: 8px 0;
            font-size: 1.1em;
            color: var(--medium-text);
            opacity: 0.4;
            transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transform: translateX(-20px);
        }
        
        .loading-step.active {
            opacity: 1;
            color: var(--soft-purple);
            font-weight: 600;
            transform: translateX(0) scale(1.05);
            background: rgba(163, 136, 199, 0.1);
            border-color: rgba(163, 136, 199, 0.3);
            box-shadow: 
                0 8px 25px rgba(163, 136, 199, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }
        
        .loading-step.active .step-icon {
            animation: iconPulse 1.5s ease-in-out infinite;
            filter: drop-shadow(0 0 12px rgba(163, 136, 199, 0.6));
            transform: scale(1.2);
        }
          .loading-step.completed {
            opacity: 0.9;
            color: var(--soft-green);
            transform: translateX(0) scale(0.95);
            background: rgba(133, 196, 181, 0.1);
            border-color: rgba(133, 196, 181, 0.3);
        }
        
        .loading-step.completed .step-icon {
            animation: checkmark 0.6s ease-out;
            filter: drop-shadow(0 0 8px rgba(133, 196, 181, 0.4));
            color: var(--soft-green);
        }
        
        @keyframes iconPulse {
            0%, 100% { 
                transform: scale(1.2);
                filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
            }
            50% { 
                transform: scale(1.4);
                filter: drop-shadow(0 4px 8px rgba(163, 136, 199, 0.5));
            }
        }
        
        @keyframes checkmark {
            0% { transform: scale(1.2); }
            50% { transform: scale(1.6) rotate(10deg); }
            100% { transform: scale(1.2) rotate(0deg); }
        }
        
        .step-icon {
            font-size: 1.4em;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            min-width: 28px;
            text-align: center;
            position: relative;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
        }
        
        .progress-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--soft-purple), var(--soft-blue), var(--soft-green));
            border-radius: 2px;
            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0 10px rgba(163, 136, 199, 0.5);
        }
        
        .step-dots {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin: 25px 0;
            position: relative;
            z-index: 2;
        }
        
        .dot {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: rgba(163, 136, 199, 0.3);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            border: 2px solid rgba(255, 255, 255, 0.5);
        }
        
        .dot.active {
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            transform: scale(1.4);
            box-shadow: 
                0 0 20px rgba(163, 136, 199, 0.7),
                inset 0 2px 4px rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.8);
        }
        
        .dot.active::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 24px;
            height: 24px;
            border: 2px solid rgba(163, 136, 199, 0.4);
            border-radius: 50%;
            animation: ripple 1.8s ease-out infinite;
        }
        
        .dot.completed {
            background: linear-gradient(135deg, var(--soft-green), var(--soft-blue));
            transform: scale(1.2);
            border-color: rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 15px rgba(133, 196, 181, 0.6);
        }
        
        @keyframes ripple {
            0% {
                transform: translate(-50%, -50%) scale(1);
                opacity: 0.8;
            }
            100% {
                transform: translate(-50%, -50%) scale(2.5);
                opacity: 0;
            }
        }
          /* Enhanced responsive design for loading */
        @media (max-width: 768px) {
            .playlist-generator {
                padding: 25px 20px;
                margin: 20px auto;
                width: 95%;
            }
            
            .vinyl-record {
                display: none;
            }
            
            .loading-text {
                font-size: 1.3em;
            }
            
            .loading-step {
                padding: 12px 15px;
                font-size: 1em;
            }
            
            .music-visualizer {
                height: 80px;
                gap: 6px;
            }
            
            .bar {
                width: 5px;
            }
            
            .floating-notes {
                display: none;
            }
            
            .logout-btn {
                position: fixed;
                top: 15px;
                right: 15px;
                z-index: 1000;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 20px;
            }
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
            position: absolute;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 500;
            font-size: 14px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .logout-btn:hover {
            background: linear-gradient(135deg, #764ba2, #667eea);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            text-decoration: none;
            color: white;
        }

        .logout-btn:active {
            transform: translateY(0);
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
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
            width: 20px;
            height: 20px;
            background: transparent;
            border: none;
            cursor: pointer;
        }
        
        .slider::-moz-range-thumb {
            width: 20px;
            height: 20px;
            background: transparent;
            border: none;
            cursor: pointer;
            -moz-appearance: none;
        }
        
        .slider::-ms-thumb {
            width: 20px;
            height: 20px;
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
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
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
            flex-direction: column; /* Stack items vertically */
            align-items: center; /* Center horizontally */
            justify-content: center; /* Center vertically */
            gap: 15px;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .detail-content, .link-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 5px;
            align-items: center; /* Changed from flex-start to center */
            text-align: center; /* Add this to center text content */
        }
        
        .playlist-link-card .link-icon {
            font-size: 1.8em;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .playlist-link-card .link-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            text-align: center; /* Ensure text is centered */
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
            filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
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
        
        /* Preferences Toggle Styles */
        .preferences-container {
            background: linear-gradient(135deg, rgba(163, 136, 199, 0.08), rgba(123, 184, 217, 0.08));
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 25px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .preferences-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(163, 136, 199, 0.05), transparent);
            animation: shimmer 4s ease-in-out infinite;
            transform: rotate(45deg);
        }
        
        .preferences-toggle-wrapper {
            display: flex;
            justify-content: center;
            margin-bottom: 15px;
            position: relative;
            z-index: 2;
        }
        
        .preferences-toggle {
            display: flex;
            align-items: center;
            gap: 20px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            color: var(--dark-text);
            padding: 15px 25px;
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }
        
        .preferences-toggle:hover {
            background: rgba(255, 255, 255, 0.8);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(163, 136, 199, 0.15);
        }
        
        .preferences-toggle input[type="checkbox"] {
            display: none;
        }
        
        .toggle-slider {
            position: relative;
            width: 60px;
            height: 32px;
            background: rgba(163, 136, 199, 0.2);
            border-radius: 16px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            flex-shrink: 0;
            border: 2px solid rgba(255, 255, 255, 0.3);
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .toggle-slider::before {
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            border-radius: 50%;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 
                0 2px 8px rgba(0, 0, 0, 0.15),
                0 1px 3px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(163, 136, 199, 0.1);
        }
        
        .preferences-toggle input:checked + .toggle-slider {
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            border-color: rgba(255, 255, 255, 0.5);
            box-shadow: 
                inset 0 2px 4px rgba(0, 0, 0, 0.1),
                0 0 20px rgba(163, 136, 199, 0.3);
        }
        
        .preferences-toggle input:checked + .toggle-slider::before {
            transform: translateX(28px);
            background: linear-gradient(135deg, #ffffff, #f0f8ff);
            box-shadow: 
                0 3px 12px rgba(0, 0, 0, 0.2),
                0 1px 4px rgba(0, 0, 0, 0.1);
        }
        
        .toggle-text {
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 1;
        }
        
        .toggle-icon {
            font-size: 1.4em;
            background: linear-gradient(135deg, var(--soft-purple), var(--soft-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
            animation: iconPulse 3s ease-in-out infinite;
        }
        
        @keyframes iconPulse {
            0%, 100% { 
                transform: scale(1);
                filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
            }
            50% { 
                transform: scale(1.1);
                filter: drop-shadow(0 4px 8px rgba(163, 136, 199, 0.5));
            }
        }
        
        .preferences-description {
            margin-top: 15px;
            font-size: 0.95em;
            color: var(--medium-text);
            font-style: italic;
            line-height: 1.5;
            text-align: center;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
            position: relative;
            z-index: 2;
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(5px);
            padding: 12px 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .preferences-description::before {
            content: '💡';
            margin-right: 8px;
            font-style: normal;
            opacity: 0.8;
        }
        
        .preferences-container:hover {
            background: linear-gradient(135deg, rgba(163, 136, 199, 0.12), rgba(123, 184, 217, 0.12));
            transform: translateY(-2px);
            box-shadow: 
                0 12px 35px rgba(0, 0, 0, 0.12),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
        }
        
        /* Add a subtle glow effect when toggle is active */
        .preferences-toggle input:checked ~ .toggle-text .toggle-icon {
            animation: iconGlow 2s ease-in-out infinite;
        }
        
        @keyframes iconGlow {
            0%, 100% { 
                filter: drop-shadow(0 2px 4px rgba(163, 136, 199, 0.3));
            }
            50% { 
                filter: drop-shadow(0 4px 12px rgba(163, 136, 199, 0.6));
            }
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .preferences-toggle {
                flex-direction: column;
                gap: 15px;
                text-align: center;
                padding: 20px;
            }
            
            .toggle-text {
                justify-content: center;
                order: -1;
            }
            
            .preferences-description {
                font-size: 0.9em;
                padding: 10px 15px;
            }
            
            .preferences-container {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <!-- Add logout button at the top -->
    <a href="/auth/logout" class="logout-btn">Logout</a>
    
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
            <div class="example"><strong>Very Detailed:</strong> "There are few people whom I really love, and still fewer of whom I think well. The more I see of the world, the more am I dissatisfied with it; and every day confirms my belief of the inconsistency of all human characters, and of the little dependence that can be placed on the appearance of merit or sense."</div>        </div>
          <!-- Authentication Section - User Info Only -->
        <div id="user-section" class="auth-section" style="display: none;">
            <div class="user-info">
                <img id="user-avatar" src="" alt="User Avatar" style="width: 50px; height: 50px; border-radius: 50%; margin-bottom: 10px; display: none;">
                <span>Welcome, <span id="user-name">User</span>!</span>
            </div>
        </div>
        
        <form id="playlistForm">
            <textarea id="prompt" placeholder="Describe your perfect playlist moment... The more details you provide (mood, setting, activity, time of day, weather, specific feelings, musical preferences), the more tailored your playlist will be!"></textarea>
            <input type="text" id="playlistName" placeholder="Playlist name (optional - AI will generate one based on your description)">
            
            <!-- Minimalist Song Count Slider -->
            <div class="song-count-container" style="margin: 20px 0;">
                <label for="songCount" class="slider-label">Songs: <span id="songCountValue">20</span></label>
                <div class="slider-wrapper">
                    <span class="slider-min">10</span>
                    <div class="custom-slider">
                        <input type="range" id="songCount" min="10" max="30" value="20" step="0.1" class="slider">
                        <div class="slider-thumb"></div>
                    </div>
                    <span class="slider-max">30</span>
                </div>
            </div>
            
            <!-- Preferences Toggle -->
            <div class="preferences-container" style="margin: 25px 0;">
                <div class="preferences-toggle-wrapper">
                    <label class="preferences-toggle">
                        <input type="checkbox" id="usePreferences" checked>
                        <span class="toggle-slider"></span>
                        <span class="toggle-text">
                            <span class="toggle-icon">🎵</span>
                            Use my Spotify listening history for personalized recommendations
                        </span>
                    </label>
                </div>
                <p class="preferences-description">
                    This analyzes your top artists, genres, and listening patterns to create more tailored playlists
                </p>
            </div>
            
            <button type="submit">Make My Playlist</button>
        </form>
        
        <div class="loading" id="loading">🎵 Analyzing your prompt and crafting the perfect playlist... This may take a moment.</div>
        <div id="result"></div>
    </div>

    <script>
        // Song count slider functionality
        const songSlider = document.getElementById('songCount');
        const songCountValue = document.getElementById('songCountValue');
        const sliderThumb = document.querySelector('.slider-thumb');
        
        function updateSlider() {
            const rawValue = parseFloat(songSlider.value);
            const intValue = Math.round(rawValue); // Round to nearest integer for display
            songCountValue.textContent = intValue;
            
            // Calculate position for slider thumb using the raw float value for smooth positioning
            const percentage = ((rawValue - 10) / (30 - 10)) * 100;
            sliderThumb.style.left = `${percentage}%`;
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
            const songCount = Math.round(parseFloat(document.getElementById('songCount').value)) || 20;
            const usePreferences = document.getElementById('usePreferences').checked;
            const submitButton = document.querySelector('button[type="submit"]');
            
            // Validate song count (using the rounded integer value)
            if (songCount < 10 || songCount > 30) {
                alert('Please select a number between 10 and 30 songs');
                return;
            }
            
            if (!prompt.trim()) {
                alert('Please enter a prompt!');
                return;
            }
            
            // Disable button and show loading
            submitButton.disabled = true;
            submitButton.textContent = 'Creating Playlist...';
            document.getElementById('loading').style.display = 'none';
            document.getElementById('result').innerHTML = '';
            
            // Show cool animation
            showPlaylistGenerator();
            
            // Auto-scroll to the loading animation after a brief delay
            setTimeout(() => {
                const generatorElement = document.getElementById('playlistGenerator');
                if (generatorElement) {
                    generatorElement.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' // Center the loader in the viewport
                    });
                }
            }, 200); // Small delay to ensure the loader is rendered
            
            try {
                const response = await fetch('/create-playlist', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        prompt, 
                        playlist_name: playlistName,
                        song_count: songCount,
                        use_preferences: usePreferences
                    })
                });
                
                const data = await response.json();
                hidePlaylistGenerator();
                
                if (data.error) {
                    document.getElementById('result').innerHTML = `<div style="color: red;">Error: ${data.error}</div>`;
                    // Scroll to error message
                    setTimeout(() => {
                        const resultElement = document.getElementById('result');
                        if (resultElement) {
                            resultElement.scrollIntoView({ 
                                behavior: 'smooth', 
                                block: 'center' 
                            });
                        }
                    }, 100);
                } else {
                    displayResult(data);
                }
            } catch (error) {
                hidePlaylistGenerator();
                document.getElementById('result').innerHTML = `<div style="color: red;">Error: ${error.message}</div>`;
                // Scroll to error message
                setTimeout(() => {
                    const resultElement = document.getElementById('result');
                    if (resultElement) {
                        resultElement.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'center' 
                        });
                    }
                }, 100);
            } finally {
                // Re-enable button
                submitButton.disabled = false;
                submitButton.textContent = 'Make My Playlist';
            }
        });
        
        function showPlaylistGenerator() {
            const generatorHtml = `
                <div class="playlist-generator" id="playlistGenerator">
                    <div class="floating-notes">
                        <div class="note">♪</div>
                        <div class="note">♫</div>
                        <div class="note">♪</div>
                        <div class="note">♬</div>
                        <div class="note">♪</div>
                        <div class="note">♫</div>
                        <div class="note">♪</div>
                        <div class="note">♬</div>
                    </div>
                    
                    <div class="vinyl-record"></div>
                    
                    <div class="loading-text">Crafting Your Perfect Playlist</div>
                    
                    <div class="music-visualizer">
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                    </div>
                    
                    <div class="step-dots">
                        <div class="dot active" id="dot1"></div>
                        <div class="dot" id="dot2"></div>
                        <div class="dot" id="dot3"></div>
                        <div class="dot" id="dot4"></div>
                        <div class="dot" id="dot5"></div>
                    </div>
                    
                    <ul class="loading-steps">
                        <li class="loading-step active" id="step1">
                            <span class="step-icon">🔍</span>
                            <span>Analyzing your prompt and extracting mood...</span>
                        </li>
                        <li class="loading-step" id="step2">
                            <span class="step-icon">🎭</span>
                            <span>Understanding emotions and musical preferences...</span>
                        </li>
                        <li class="loading-step" id="step3">
                            <span class="step-icon">🎵</span>
                            <span>Searching Spotify's vast music library...</span>
                        </li>
                        <li class="loading-step" id="step4">
                            <span class="step-icon">📝</span>
                            <span>Creating and customizing your playlist...</span>
                        </li>
                        <li class="loading-step" id="step5">
                            <span class="step-icon">✨</span>
                            <span>Adding final touches and saving to your library...</span>
                        </li>
                    </ul>
                    
                    <div class="progress-bar" style="width: 20%;"></div>
                </div>
            `;
            
            document.getElementById('result').innerHTML = generatorHtml;
            document.getElementById('playlistGenerator').style.display = 'block';
            
            // Animate through steps
            animateLoadingSteps();
        }
        
        function hidePlaylistGenerator() {
            const generator = document.getElementById('playlistGenerator');
            if (generator) {
                generator.style.display = 'none';
            }
        }
        
        function animateLoadingSteps() {
            const steps = ['step1', 'step2', 'step3', 'step4', 'step5'];
            const dots = ['dot1', 'dot2', 'dot3', 'dot4', 'dot5'];
            let currentStep = 0;
            
            const stepInterval = setInterval(() => {
                // Update progress bar
                const progressBar = document.querySelector('.progress-bar');
                if (progressBar) {
                    progressBar.style.width = `${((currentStep + 1) / steps.length) * 100}%`;
                }
                
                // Mark current step as completed and dot as completed
                if (currentStep > 0) {
                    const prevStep = document.getElementById(steps[currentStep - 1]);
                    const prevDot = document.getElementById(dots[currentStep - 1]);
                    if (prevStep) {
                        prevStep.classList.remove('active');
                        prevStep.classList.add('completed');
                        
                        // Change icon to checkmark for completed steps
                        const icon = prevStep.querySelector('.step-icon');
                        if (icon) {
                            icon.textContent = '✓';
                        }
                    }
                    if (prevDot) {
                        prevDot.classList.remove('active');
                        prevDot.classList.add('completed');
                    }
                }
                
                // Activate next step and dot
                if (currentStep < steps.length) {
                    const nextStep = document.getElementById(steps[currentStep]);
                    const nextDot = document.getElementById(dots[currentStep]);
                    if (nextStep) {
                        nextStep.classList.add('active');
                    }
                    if (nextDot) {
                        nextDot.classList.add('active');
                    }
                    currentStep++;
                } else {
                    clearInterval(stepInterval);
                    
                    // Complete the progress bar
                    if (progressBar) {
                        progressBar.style.width = '100%';
                    }
                }
            }, 1800); // Slightly longer intervals for better visual effect
        }
        
        function displayResult(data) {
            const analysis = data.analysis;
            const songs = data.songs;
            const playlist = data.playlist;
            
            // Count personalized songs
            const personalizedSongs = songs.filter(song => 
                song.reason && song.reason.toLowerCase().includes('personalized')
            ).length;
            
            // Build preferences section if used
            let preferencesSection = '';
            if (analysis.used_preferences && analysis.user_preferences_summary) {
                const prefs = analysis.user_preferences_summary;
                preferencesSection = `
                    <div class="analysis-card">
                        <h4>🎯 Personalization Applied</h4>
                        <p><strong>Your Top Artists:</strong> ${prefs.top_artists.map(a => `<span class="tag">${a}</span>`).join('')}</p>
                        <p><strong>Your Genres:</strong> ${prefs.top_genres.map(g => `<span class="tag">${g}</span>`).join('')}</p>
                        ${prefs.audio_profile.average_tempo ? `<p><strong>Your Tempo:</strong> ${prefs.audio_profile.average_tempo} BPM</p>` : ''}
                        ${prefs.audio_profile.valence_score ? `<p><strong>Your Positivity:</strong> ${(prefs.audio_profile.valence_score * 100).toFixed(0)}%</p>` : ''}
                        ${personalizedSongs > 0 ? `<p><strong>Personalized Picks:</strong> ${personalizedSongs} songs tailored to your taste</p>` : ''}
                    </div>
                `;
            }
            
            const html = `
                <div class="result">
                    <div class="playlist-header">
                        <div class="success-icon">🎵</div>
                        <h3 class="success-title">Playlist Created Successfully!</h3>
                        <div class="playlist-name">"${playlist.name}"</div>
                        ${analysis.used_preferences ? '<p style="color: var(--soft-purple); font-style: italic;">✨ Personalized with your listening history</p>' : ''}
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
                        ${preferencesSection}
                        
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
            
            // Smooth scroll to the result section after a brief delay to ensure rendering
            setTimeout(() => {
                const resultElement = document.getElementById('result');
                if (resultElement) {
                    resultElement.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' // Start at the top of the results
                    });
                }
            }, 300); // Small delay to ensure the content is fully rendered
        }        function showLoginSection() {
            // Redirect to login page instead of showing login section on main page
            window.location.href = '/login';
        }

        function showUserSection(user) {
            document.getElementById('user-section').style.display = 'block';
            
            // Enable the form
            document.getElementById('playlistForm').style.opacity = '1';
            document.getElementById('playlistForm').style.pointerEvents = 'auto';
              // Update user info
            const userName = document.getElementById('user-name');
            const userAvatar = document.getElementById('user-avatar');
            
            if (userName) {
                userName.textContent = user.name || 'User';
            }
            
            if (userAvatar && user.image) {
                userAvatar.src = user.image;
                userAvatar.style.display = 'block';
            }
        }

        function logout() {
            window.location.href = '/auth/logout';
        }        async function createPlaylist() {
            // Check if user is authenticated with better error handling
            try {
                const authResponse = await fetch('/api/user', {
                    credentials: 'same-origin',
                    cache: 'no-cache'
                });
                
                if (!authResponse.ok) {
                    if (authResponse.status === 401) {
                        console.log('User not authenticated for playlist creation, redirecting to login');
                        window.location.href = '/login';
                        return;
                    } else {
                        showError('Authentication check failed. Please try refreshing the page.');
                        return;
                    }
                }
            } catch (error) {
                console.error('Auth check failed:', error);
                showError('Unable to verify authentication. Please check your connection and try again.');
                return;
            }
            // ...rest of playlist creation code...
        }async function loadUserInfo() {
            // Prevent multiple simultaneous auth checks
            if (window.authCheckInProgress) {
                console.log('Auth check already in progress, skipping...');
                return;
            }
            
            window.authCheckInProgress = true;
              try {
                console.log('Loading user info...');
                const response = await fetch('/api/user', {
                    credentials: 'same-origin', // Ensure cookies are sent
                    cache: 'no-cache' // Prevent caching of auth state
                });
                console.log('Auth response status:', response.status);
                console.log('Auth response headers:', [...response.headers.entries()]);
                
                if (response.ok) {
                    const data = await response.json();
                    console.log('User authenticated:', data.user.name);
                    showUserSection(data.user);
                } else if (response.status === 401) {
                    console.log('User not authenticated (401), redirecting to login');
                    const responseText = await response.text();
                    console.log('401 Response body:', responseText);
                    // Only redirect if we're not already on the login page
                    if (!window.location.pathname.includes('/login')) {
                        setTimeout(() => {
                            window.location.href = '/login';
                        }, 1000);
                    }
                } else {
                    console.log('Unexpected auth response:', response.status);
                    const responseText = await response.text();
                    console.log('Response body:', responseText);
                    // For other errors, show user section with limited functionality
                    showUserSection({ name: 'User', image: '' });
                }
            } catch (error) {
                console.error('Failed to load user info:', error);
                // Only redirect on network errors if we're not already on login page
                if (!window.location.pathname.includes('/login')) {
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 1000);
                }
            } finally {
                window.authCheckInProgress = false;
            }
        }        // Call this when the page loads - only once
        document.addEventListener('DOMContentLoaded', function() {
            // Check if we just came from a login redirect
            const urlParams = new URLSearchParams(window.location.search);
            const fromLogin = urlParams.get('from') === 'login';
              if (fromLogin) {
                // Remove the parameter from URL
                const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
                window.history.replaceState({}, document.title, newUrl);
                
                // Give extra time for session to be established after login
                console.log('Post-login flow detected, waiting 3 seconds for session...');
                setTimeout(loadUserInfo, 3000);
            } else {
                // Normal page load
                loadUserInfo();
            }
        });
    </script>
</body>
</html>
"""