import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import random

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
        if "open google" in command:
            self.speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "open youtube" in command:
            self.speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "what time" in command or "current time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {now}")
        elif "search wikipedia for" in command:
            topic = command.replace("search wikipedia for", "").strip()
            if topic:
                try:
                    summary = wikipedia.summary(topic, sentences=2)
                    self.speak(summary)
                except Exception:
                    self.speak("Sorry, I couldn't find information on that topic.")
            else:
                self.speak("Please specify a topic to search for.")
        elif "tell me a joke" in command or "joke" in command:
            joke = random.choice(self.jokes)
            self.speak(joke)
        elif "goodbye" in command or "stop listening" in command or "exit" in command:
            self.speak("Goodbye!")
            return False
        else:
            self.speak("Sorry, I don't recognize that command.")
        return True

    def listen_and_respond(self):
        self.speak("Hello! How can I help you today?")
        running = True
        while running:
            command = self.listen()
            if command:
                running = self.handle_command(command)