import os
import webbrowser
import datetime
import pyttsx3
import pyjokes
import wikipedia

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    command = command.lower()

    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time}")
        print(f"Assistant: The current time is {time}")

    elif "date" in command:
        date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {date}")
        print(f"Assistant: Today's date is {date}")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)
        print(f"Assistant: {joke}")

    elif "wikipedia" in command:
        try:
            topic = command.replace("wikipedia", "").strip()
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
            print(f"Assistant: {summary}")
        except Exception:
            speak("Sorry, I could not fetch information right now.")
            print("Assistant: Sorry, I could not fetch information right now.")

    elif "open notepad" in command:
        os.system("notepad.exe")
        speak("Opening Notepad")
        print("Assistant: Opening Notepad")

    elif "open calculator" in command:
        os.system("calc.exe")
        speak("Opening Calculator")
        print("Assistant: Opening Calculator")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
        print("Assistant: Opening Google")

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
        print("Assistant: Opening YouTube")

    elif "good morning" in command:
        speak("Good morning! How can I help you today?")
        print("Assistant: Good morning! How can I help you today?")

    elif "goodbye" in command or "exit" in command:
        speak("Goodbye!")
        print("Assistant: Goodbye!")
        exit()

    else:
        speak("Sorry, I didn’t understand that. Can you repeat?")
        print("Assistant: Sorry, I didn’t understand that. Can you repeat?")
