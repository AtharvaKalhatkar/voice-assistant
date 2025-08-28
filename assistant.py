import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import random
import difflib

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.jokes = [
            "Why did the computer show up at work late? It had a hard drive.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why was the cell phone wearing glasses? It lost its contacts."
        ]

    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                print(f"You said: {command}")
                return command.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I could not understand.")
            except sr.RequestError:
                self.speak("Sorry, I am having trouble connecting to the service.")
            return ""

    def handle_command(self, command):
        print(f"Recognized command: {command}")
        # Trigger phrases for each feature
        commands = {
            "open_google": ["open google", "open browser", "google"],
            "open_youtube": ["open youtube", "youtube"],
            "get_time": ["what's the time", "tell me the time", "current time", "time"],
            "search_wikipedia": ["search wikipedia for", "wikipedia"],
            "tell_joke": ["tell me a joke", "joke"],
            "exit": ["goodbye", "stop listening", "exit", "bye"],
            "greeting": ["hello", "hi"]
        }
        # Use difflib to find closest match
        for key, phrases in commands.items():
            for phrase in phrases:
                if difflib.SequenceMatcher(None, phrase, command).ratio() > 0.7 or phrase in command:
                    if key == "open_google":
                        self.speak("Opening Google")
                        webbrowser.open("https://www.google.com")
                        return True
                    elif key == "open_youtube":
                        self.speak("Opening YouTube")
                        webbrowser.open("https://www.youtube.com")
                        return True
                    elif key == "get_time":
                        now = datetime.datetime.now().strftime("%I:%M %p")
                        self.speak(f"The current time is {now}")
                        return True
                    elif key == "search_wikipedia":
                        topic = command.replace(phrase, "").strip()
                        if topic:
                            try:
                                summary = wikipedia.summary(topic, sentences=2)
                                self.speak(summary)
                            except Exception:
                                self.speak("Sorry, I couldn't find information on that topic.")
                        else:
                            self.speak("Please specify a topic to search for.")
                        return True
                    elif key == "tell_joke":
                        joke = random.choice(self.jokes)
                        self.speak(joke)
                        return True
                    elif key == "exit":
                        self.speak("Goodbye!")
                        return False
                    elif key == "greeting":
                        self.speak("Hello! How can I help you?")
                        return True
        # No match found
        self.speak("Sorry, I don't recognize that command.")
        return True

    def listen_and_respond(self):
        self.speak("Hello! How can I help you today?")
        running = True
        while running:
            command = self.listen()
            if command:
                running = self.handle_command(command)