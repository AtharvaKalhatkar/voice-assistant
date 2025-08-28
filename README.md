# Voice Assistant - Ultimate Edition

## Features

- Voice recognition and text-to-speech responses
- Weather information (OpenWeatherMap API required)
- News headlines (NewsAPI required)
- Reminders (“Remind me to [task] at [time]”)
- To-Do list (“Add [task] to my to-do list”, “Show my to-do list”)
- Play music on YouTube (“Play [song name]”)
- Calculator/Math (“Calculate [expression]”, “What is [expr]”)
- Open applications (“Open Notepad”, “Open Chrome”)
- Set timers/alarms (“Set a timer for [seconds]”, “Set an alarm for [time]”)
- General knowledge questions (“Who is [person]”, “What is [thing]”)
- Language translation (“Translate [word] to [language]”)
- Read out a text file (“Read my document”)
- Tells jokes (“Tell me a joke”, “Joke”)
- Responds to greetings (“Hello”, “Hi”)
- Exits on (“Goodbye”, “Exit”, “Stop listening”, “Bye”)

## Setup

- Install requirements:  
  `pip install -r requirements.txt`
- Add your API keys in `assistant.py` for weather and news.

## Usage

- Run:  
  `python main.py`
- Try speaking any of the commands above!

## Notes

- For translation, you need internet connectivity.
- For weather/news, sign up at [OpenWeatherMap](https://openweathermap.org/api) and [NewsAPI](https://newsapi.org/) for free API keys.