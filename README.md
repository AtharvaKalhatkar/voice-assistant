<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Voice Assistant with GUI</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 40px;
      background: #0f172a;
      color: #e2e8f0;
      line-height: 1.6;
    }
    h1, h2, h3 {
      color: #38bdf8;
    }
    pre {
      background: #1e293b;
      padding: 10px;
      border-radius: 6px;
      overflow-x: auto;
    }
    code {
      color: #fbbf24;
      font-weight: bold;
    }
    ul {
      list-style: square;
    }
    .box {
      background: #1e293b;
      padding: 15px;
      border-radius: 8px;
      margin: 15px 0;
      box-shadow: 0 0 10px #38bdf8;
    }
  </style>
</head>
<body>

  <h1>🎤 Voice Assistant with GUI</h1>
  <p>
    A Python-based Voice Assistant that can perform various tasks such as opening apps, 
    answering general knowledge questions, and chatting with users.  
    It comes with a modern <strong>Tkinter GUI</strong> for an interactive experience.
  </p>

  <h2>🚀 Features</h2>
  <div class="box">
    <ul>
      <li>🎙️ <b>Voice Recognition</b> – Continuously listens and processes user commands.</li>
      <li>🗣️ <b>Text-to-Speech</b> – Assistant talks back with natural speech.</li>
      <li>💻 <b>App Control</b> – Open system apps and websites with voice commands.</li>
      <li>🌐 <b>General Knowledge</b> – Answer questions using Wikipedia and APIs.</li>
      <li>🤝 <b>Casual Chat</b> – Responds to greetings and general talk (e.g., "hi", "how are you").</li>
      <li>🎨 <b>Modern GUI</b> – Attractive glowing Tkinter interface.</li>
    </ul>
  </div>

  <h2>🛠️ Installation</h2>
  <ol>
    <li><b>Clone the Repository</b>
      <pre><code>git clone https://github.com/AtharvaKalhatkar/voice-assistant.git
cd voice-assistant</code></pre>
    </li>
    <li><b>Create Virtual Environment (Optional)</b>
      <pre><code>python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Linux/Mac</code></pre>
    </li>
    <li><b>Install Dependencies</b>
      <pre><code>pip install -r requirements.txt</code></pre>
    </li>
  </ol>

  <h2>▶️ Usage</h2>
  <p>Run the assistant with:</p>
  <pre><code>python ui.py</code></pre>

  <p>Example commands:</p>
  <ul>
    <li><code>open Google</code> → Opens Google in your browser.</li>
    <li><code>who is Albert Einstein</code> → Gives Wikipedia summary.</li>
    <li><code>hi</code> / <code>hello</code> → Assistant greets you back.</li>
  </ul>

  <h2>📂 Project Structure</h2>
  <pre><code>voice-assistant/
│── assistant.py     # Core logic & command handling
│── ui.py            # Tkinter-based GUI
│── requirements.txt # Python dependencies
│── README.html      # Project documentation</code></pre>

  <h2>🧩 Requirements</h2>
  <ul>
    <li>Python <b>3.9+</b></li>
    <li>Libraries:
      <ul>
        <li>speechrecognition</li>
        <li>pyttsx3</li>
        <li>wikipedia</li>
        <li>tkinter (built-in)</li>
        <li>pyaudio</li>
      </ul>
    </li>
  </ul>

  <p>Install all dependencies via:</p>
  <pre><code>pip install -r requirements.txt</code></pre>

  <h2>📸 Screenshots</h2>
  <p><i>(Add screenshots of your UI here)</i></p>

  <h2>🤝 Contributing</h2>
  <p>
    Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve.
  </p>

  <h2>📜 License</h2>
  <p>
    This project is licensed under the <b>MIT License</b> – feel free to use and modify.
  </p>

  <hr>
  <p>👨‍💻 Developed by <b>Atharva Kalhatkar</b></p>

</body>
</html>
