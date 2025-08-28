import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import random
import difflib
import requests
from googletrans import Translator

# --- API KEYS: Insert your own ---
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.jokes = [
            "Why did the computer show up at work late? It had a hard drive.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why was the cell phone wearing glasses? It lost its contacts."
        ]
        self.todo = []
        self.translator = Translator()
        self.reminders = []
        self.alarms = []

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

    # --- Feature: Weather ---
    def get_weather(self, city):
        if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
            self.speak("Weather API key not set.")
            return
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get("main"):
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                self.speak(f"The weather in {city} is {desc} with a temperature of {temp} degrees Celsius.")
            else:
                self.speak("Sorry, I couldn't find the weather for that city.")
        except Exception:
            self.speak("Failed to get weather information.")

    # --- Feature: News ---
    def get_news(self):
        if not NEWS_API_KEY or NEWS_API_KEY == "YOUR_NEWSAPI_KEY":
            self.speak("News API key not set.")
            return
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        try:
            response = requests.get(url)
            data = response.json()
            articles = data.get("articles", [])
            if articles:
                self.speak("Here are the top news headlines:")
                for article in articles[:3]:
                    self.speak(article["title"])
            else:
                self.speak("Sorry, I couldn't find any news.")
        except Exception:
            self.speak("Failed to get news information.")

    # --- Feature: Reminders ---
    def add_reminder(self, task, time):
        self.reminders.append((task, time))
        self.speak(f"Reminder set for {task} at {time}.")

    # --- Feature: To-Do List ---
    def add_todo(self, task):
        self.todo.append(task)
        self.speak(f"Added {task} to your to-do list.")

    def list_todo(self):
        if self.todo:
            self.speak("Your to-do list includes:")
            for item in self.todo:
                self.speak(item)
        else:
            self.speak("Your to-do list is empty.")

    # --- Feature: Play Music ---
    def play_music(self, query):
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        self.speak(f"Playing {query} on YouTube.")
        webbrowser.open(url)

    # --- Feature: Calculator/Math ---
    def calculate(self, expression):
        try:
            result = eval(expression)
            self.speak(f"The answer is {result}.")
        except Exception:
            self.speak("Sorry, I can't calculate that.")

    # --- Feature: Open Applications ---
    def open_application(self, app):
        import os
        if app in ["notepad"]:
            os.system("notepad.exe")
            self.speak("Opening Notepad.")
        elif app in ["chrome", "google chrome"]:
            os.system("start chrome")
            self.speak("Opening Chrome.")
        else:
            self.speak("Application not recognized.")

    # --- Feature: Set Alarms/Timers ---
    def set_timer(self, seconds):
        import time
        self.speak(f"Timer set for {seconds} seconds.")
        time.sleep(int(seconds))
        self.speak(f"Timer finished after {seconds} seconds!")

    def set_alarm(self, alarm_time):
        self.alarms.append(alarm_time)
        self.speak(f"Alarm set for {alarm_time}. (Note: This is a reminder only, not an actual alarm sound.)")

    # --- Feature: General Knowledge Q&A ---
    def general_knowledge(self, query):
        try:
            summary = wikipedia.summary(query, sentences=2)
            self.speak(summary)
        except Exception:
            self.speak("Sorry, I couldn't find information on that topic.")

    # --- Feature: Language Translation ---
    def translate(self, text, dest_lang):
        try:
            result = self.translator.translate(text, dest=dest_lang)
            self.speak(f"{text} in {dest_lang} is {result.text}")
        except Exception:
            self.speak("Sorry, I couldn't translate that.")

    # --- Feature: Read Text File ---
    def read_text_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read(300)
                self.speak(f"The content is: {content}")
        except Exception:
            self.speak("Sorry, I couldn't read that file.")

    def handle_command(self, command):
        print(f"Recognized command: {command}")
        # Weather
        if "weather in" in command:
            city = command.split("weather in")[-1].strip()
            self.get_weather(city)
        # News
        elif "news" in command or "headlines" in command:
            self.get_news()
        # Reminder
        elif "remind me to" in command and "at" in command:
            try:
                task = command.split("remind me to")[1].split("at")[0].strip()
                time = command.split("at")[1].strip()
                self.add_reminder(task, time)
            except Exception:
                self.speak("Please specify the reminder in format: Remind me to [task] at [time].")
        # To-Do
        elif "add" in command and "to my to-do list" in command:
            task = command.split("add")[1].split("to my to-do list")[0].strip()
            self.add_todo(task)
        elif "show my to-do list" in command or "list my to-do" in command:
            self.list_todo()
        # Music
        elif "play" in command and "music" in command:
            self.play_music("music")
        elif "play" in command:
            song = command.replace("play", "").strip()
            self.play_music(song)
        # Calculator/Math
        elif "calculate" in command:
            expr = command.replace("calculate", "").strip()
            self.calculate(expr)
        elif "what is" in command:
            expr = command.replace("what is", "").strip()
            self.calculate(expr)
        # Open Applications
        elif "open" in command and ("notepad" in command or "chrome" in command):
            if "notepad" in command:
                self.open_application("notepad")
            elif "chrome" in command:
                self.open_application("chrome")
        # Timer
        elif "set a timer for" in command:
            words = command.split()
            try:
                seconds = [int(w) for w in words if w.isdigit()][0]
                self.set_timer(seconds)
            except Exception:
                self.speak("Please say: Set a timer for [number] seconds.")
        # Alarm
        elif "set an alarm for" in command:
            alarm_time = command.split("set an alarm for")[-1].strip()
            self.set_alarm(alarm_time)
        # General Knowledge
        elif "who is" in command or "what is" in command:
            query = command.replace("who is", "").replace("what is", "").strip()
            self.general_knowledge(query)
        # Translation
        elif "translate" in command and "to" in command:
            try:
                text = command.split("translate")[1].split("to")[0].strip()
                lang = command.split("to")[-1].strip()
                self.translate(text, lang)
            except Exception:
                self.speak("Say: Translate [word] to [language].")
        # Read Text File
        elif "read my document" in command or "read file" in command:
            filepath = "document.txt"  # You can change or extract filename from command
            self.read_text_file(filepath)
        # Greetings
        elif "hello" in command or "hi" in command:
            self.speak("Hello! How can I help you?")
        # Joke
        elif "joke" in command or "tell me a joke" in command:
            joke = random.choice(self.jokes)
            self.speak(joke)
        # Exit
        elif "goodbye" in command or "stop listening" in command or "exit" in command or "bye" in command:
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