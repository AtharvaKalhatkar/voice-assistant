# assistant.py
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import datetime
import os
import subprocess
import platform
import traceback

# Initialize TTS
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 165)
tts_engine.setProperty("volume", 1.0)

def speak(text: str):
    """Speak text (TTS) and also return the text so UI can display it."""
    print("Assistant:", text)
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception:
        # tts can fail on some systems; keep UI working
        print("TTS error:", traceback.format_exc())
    return text

def _open_with_path(path):
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        else:
            subprocess.Popen(["xdg-open", path])
        return True
    except Exception as e:
        print("Error opening path:", e)
        return False

def open_application(name: str):
    """Open common apps. Extend this mapping with full exe paths if needed."""
    n = name.lower()
    try:
        # Common Windows apps
        if "notepad" in n:
            os.system("notepad")
            return speak("Opening Notepad")
        if "calculator" in n or "calc" in n:
            if platform.system() == "Windows":
                os.system("calc")
            else:
                subprocess.Popen(["gnome-calculator"])
            return speak("Opening Calculator")
        if "chrome" in n or "google chrome" in n or "google" in n and "chrome" in n:
            # common chrome path on Windows; modify if necessary
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            for p in paths:
                if os.path.exists(p):
                    subprocess.Popen([p])
                    return speak("Opening Google Chrome")
            # fallback to default browser open
            webbrowser.open("https://www.google.com")
            return speak("Opening Google in browser")
        if "paint" in n:
            os.system("mspaint")
            return speak("Opening Paint")
        if "word" in n:
            # path for Office 365 Word - adjust if different
            possible = [
                r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
            ]
            for p in possible:
                if os.path.exists(p):
                    subprocess.Popen([p])
                    return speak("Opening Microsoft Word")
            return speak("Microsoft Word not found in default path.")
        # try to open as file/folder path
        if os.path.exists(name):
            ok = _open_with_path(name)
            if ok:
                return speak(f"Opening {name}")
        return speak(f"Sorry, I don't know how to open {name} yet.")
    except Exception as e:
        print("open_application error:", e)
        return speak("I faced a problem opening the application.")

def search_wikipedia(query: str):
    q = query.strip()
    if not q:
        return speak("Please tell me what to search on Wikipedia.")
    try:
        summary = wikipedia.summary(q, sentences=2, auto_suggest=True, redirect=True)
        return speak(summary)
    except wikipedia.DisambiguationError as e:
        options = e.options[:5]
        return speak(f"That query is ambiguous. Possible topics: {', '.join(options)}")
    except wikipedia.PageError:
        return speak("I couldn't find a page for that topic on Wikipedia.")
    except Exception as ex:
        print("Wikipedia error:", ex)
        return speak("Sorry, I couldn't fetch information right now.")

def process_command(command: str):
    """Process a user's command (text). Returns a response string or 'EXIT' to quit."""
    if not command or not command.strip():
        return None

    cmd = command.lower().strip()
    # --- Greetings / small talk ---
    if any(w in cmd for w in ["hi", "hello", "hii", "hey"]):
        return speak("Hey! Nice to see you. How can I help you?")
    if "how are you" in cmd:
        return speak("I'm doing well — ready to help you. How are you?")
    if "your name" in cmd or "who are you" in cmd:
        return speak("I'm your personal voice assistant built in Python.")
    if "good morning" in cmd:
        return speak("Good morning! Hope you have a great day.")
    if "good night" in cmd:
        return speak("Good night! Sleep well.")

    # --- Time / Date ---
    if "time" in cmd and "what" in cmd or cmd == "time" or "current time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return speak(f"The current time is {now}")
    if "date" in cmd and ("what" in cmd or "today" in cmd):
        today = datetime.date.today().strftime("%B %d, %Y")
        return speak(f"Today's date is {today}")

    # --- Wikipedia / General knowledge ---
    if cmd.startswith(("who is", "what is", "tell me about", "define", "explain")) or "wikipedia" in cmd:
        # sanitize
        q = cmd
        for prefix in ("who is", "what is", "tell me about", "search wikipedia for", "wikipedia", "define", "explain"):
            q = q.replace(prefix, "")
        q = q.strip()
        return search_wikipedia(q)

    # --- Open websites ---
    if "open youtube" in cmd:
        webbrowser.open("https://www.youtube.com")
        return speak("Opening YouTube")
    if "open google" in cmd:
        webbrowser.open("https://www.google.com")
        return speak("Opening Google")
    if "open github" in cmd:
        webbrowser.open("https://github.com")
        return speak("Opening GitHub")
    if "open stack overflow" in cmd or "open stackoverflow" in cmd:
        webbrowser.open("https://stackoverflow.com")
        return speak("Opening Stack Overflow")

    # --- Open apps or files ---
    if cmd.startswith("open "):
        target = cmd.replace("open ", "", 1).strip()
        # if user said "open file <name>" or "open folder <name>"
        # try basic patterns
        # attempt app open
        return open_application(target)

    # --- System commands (dangerous actions are intentionally limited) ---
    if "shutdown" in cmd and ("now" in cmd or "shutdown" == cmd):
        # We will not auto-execute shutdown to avoid misuse; inform user how to do it
        return speak("I can tell you how to shut down, but I won't run shutdown commands automatically for safety.")
    if "restart" in cmd:
        return speak("I can restart the system if you want, but that command is disabled for safety.")

    # --- Exit/Stop ---
    if any(x in cmd for x in ["exit", "quit", "stop", "goodbye", "bye"]):
        speak("Goodbye! Have a nice day.")
        return "EXIT"

    # --- Fallback ---
    return speak("Sorry, I don't understand that yet. You can ask me to open apps, search Wikipedia, open websites, or ask general questions.")
