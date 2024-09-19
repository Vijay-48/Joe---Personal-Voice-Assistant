#Packages
import speech_recognition as sr
import pyttsx3
import pyaudio
import wolframalpha
import wikipedia
import webbrowser
import ecapture as ec
import pyjokes
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
import time
import json
import base64
import email
import email.utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Initialize engine
engine = pyttsx3.init()

# Set properties for the speech engine
engine.setProperty('rate', 150) # Speed of speech
engine.setProperty('volume', 0.9) # Volume (0.0 to 1.0)

# Initialize the name of the voice assistant
assistant_name = "Joe"

# Function to speak text aloud
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get audio input from the user
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said.lower()

# Function to execute system commands
def execute_system_command(command):
    try:
        os.system(command)
    except Exception as e:
        speak("Sorry, I couldn't perform the system operation.")
        print("Exception: " + str(e))

# Function to greet the user based on the time of day
def greet_user():
    current_hour = int(datetime.now().strftime("%H"))
    if 5 <= current_hour < 12:
        speak(f"Good morning! I'm {assistant_name}. How can I assist you today?")
    elif 12 <= current_hour < 18:
        speak(f"Good afternoon! I'm {assistant_name}. How can I assist you today?")
    else:
        speak(f"Good evening! I'm {assistant_name}. How can I assist you today?")

# Function to tell jokes
def tell_joke():
    try:
        joke = pyjokes.get_joke()
        speak(joke)
    except Exception as e:
        print("Error: Failed to get joke -", e)

# Function to search Wikipedia
def search_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia, " + results)

# Function to open web browser and perform a search
def web_search(query):
    webbrowser.open("https://www.google.com/search?q=" + query)
    
# Function to set a reminder
def set_reminder(time, message):
    speak(f"Setting a reminder for {message} at {time}.")
    execute_system_command(f"remindme '{message}' at {time}")
    
# Function to play music
def play_music(query):
    execute_system_command(f"mplayer '{query}'")

# Function to add an event to the calendar
def add_event(event, date):
    speak(f"Adding {event} to the calendar on {date}.")
    execute_system_command(f"calendgear add '{event}' --date '{date}'")
    
# Function to get the latest news headlines
def get_news():
    api_key = "6036e7e108fb45e48b99b303d2c548bb"
    base_url = "https://newsapi.org/v2/top-headlines?"
    complete_url = f"{base_url}apiKey={api_key}"
    response = requests.get(complete_url)
    data = response.json()
    articles = data["articles"]
    for article in articles:
        speak(article["title"])
        
# Function to get the weather for a given location
def get_weather(location):
    api_key = "aecdc1b700e023678b340511654c14ee"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={location}"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main_data = data["main"]
        current_temperature = main_data["temp"]
        current_pressure = main_data["pressure"]
        current_humidity = main_data["humidity"]
        weather_data = data["weather"]
        weather_description = weather_data[0]["description"]
        speak(f"The current temperature is {current_temperature} degrees Celsius, with {current_humidity}% humidity and {current_pressure} hPa pressure. The weather is currently {weather_description}.")
    else:
        speak("City not found.")
        
# Function to play music on Spotifyimport requests
# Spotify API credentials
CLIENT_ID = 'your-api'
CLIENT_SECRET = 'your-secret-key'
REDIRECT_URI = 'https://open.spotify.com/'
# Define your_device_id_here with a specific device ID value
your_device_id_here = "your-device-id"

# Function to get an access token from Spotify
def get_access_token():
    auth_url = f'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    return access_token

# Function to play music on Spotify
def play_spotify(query):
    access_token = get_access_token()
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    search_url = f'https://open.spotify.com/search/{query}'
    search_response = requests.get(search_url, headers=headers)
    search_response_data = search_response.json()
    if search_response_data['tracks']['items']:
        track_uri = search_response_data['tracks']['items'][0]['uri']
        play_url = f'https://api.spotify.com/v1/me/player/play?device_id={your_device_id_here}'
        play_data = {
            'uris': [track_uri]
        }
        play_response = requests.put(play_url, headers=headers, json=play_data)


# Function to play videos on YouTube
def play_youtube(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    
# Function to get stock price
def get_stock_price(company):
    api_key = "youor-api"
    base_url = "https://www.alphavantage.co/query?"
    function = "GLOBAL_QUOTE"
    datatype = "json"
    complete_url = f"{base_url}function={function}&symbol={company}&apikey={api_key}&datatype={datatype}"
    response = requests.get(complete_url)
    data = response.json()
    if "Global Quote" in data:
        price = data["Global Quote"]["05. price"]
        return price
    else:
        return None
    
# Function to get Movie Timings
def get_movie_showtimes(movie, theater):
    api_key = "your-api"
    base_url = "https://www.themoviedb.org/movie"
    complete_url = f"{base_url}{movie}/showtimes?api_key={api_key}&language=en-US&page=1&region=US&sort_by=popularity.desc"
    response = requests.get(complete_url)
    data = response.json()
    if data:
        for showtime in data["results"]:
            if theater in showtime["venue"]["name"]:
                return showtime
    else:
        return None

# Main function to run the voice assistant
def main():
    greet_user()
    active = False

    while True:
        query = get_audio()

        if 'wake up' in query and 'Joe' in query:
            active = True
            speak("I am awake and ready for your command.")

        if active:
            if 'shutdown' in query:
                speak("Shutting down the system.")
                execute_system_command("shutdown /s /t 1")
                break

            elif 'restart' in query:
                speak("Restarting the system.")
                execute_system_command("shutdown /r /t 1")

            elif 'sleep' in query:
                speak("Putting the system to sleep.")
                execute_system_command("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif 'log off' in query:
                speak("Logging off the current user.")
                execute_system_command("shutdown /l")

            elif 'stop listening' in query:
                speak("Going back to sleep. Say 'wake up' to activate me.")
                active = False

            elif 'tell me a joke' in query:
                tell_joke()

            elif 'wikipedia' in query:
                search_wikipedia(query.replace('wikipedia', ''))

            elif 'search' in query:
                web_search(query.replace('search', ''))

            elif 'set reminder' in query:
                time = query.replace('set reminder', '')
                message = query.replace('for', '')
                set_reminder(time, message)
            elif 'play music' in query:
                music = query.replace('play music', '')
                play_music(music)
            elif 'add to calendar' in query:
                event = query.replace('add to calendar', '')
                date = query.replace('on', '')
                add_event(event, date)
                
            elif 'news' in query:
                get_news()
            
            elif 'weather' in query:
                location = query.replace('weather', '')
                get_weather(location)
                
            elif 'play on spotify' in query:
                music = query.replace('play spotify', '')
                play_spotify(music)

            elif 'play on youtube' in query:
                video = query.replace('Open youtube and play', '')
                webbrowser.open(f"https://www.youtube.com/results?search_query={video}")
      
            # Add more commands as needed

if __name__ == "__main__":
    main()
