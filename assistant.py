import speech_recognition as sr
import pyttsx3

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_and_respond(self):
        with sr.Microphone() as source:
            print("Say something...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                print(f"You said: {command}")
                self.speak(f"You said: {command}")
            except sr.UnknownValueError:
                print("Sorry, I could not understand.")
                self.speak("Sorry, I could not understand.")
            except sr.RequestError:
                print("Sorry, I am having trouble connecting to the service.")
                self.speak("Sorry, I am having trouble connecting to the service.")