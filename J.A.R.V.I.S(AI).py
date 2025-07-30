import speech_recognition as sr # now you have named speech_recognition to sr so you can directly call sr no need to call original name 
import webbrowser
import pyttsx3
import os
import music_library
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS
import pygame
import time
# Load environment variables from .env file
load_dotenv()


r = sr.Recognizer() # Creates a speech recognizer
news_api = os.getenv("NEWS_API")
# news_api = "1b3b023e389743e6ad1d421456db18b3"

# Fetch the API key securely
google_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=google_api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 20,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Use the model
model = genai.GenerativeModel(
  model_name = "gemini-1.5-flash-8b",#gemini-1.5-flash-8b / gemini-2.5-pro
  generation_config=generation_config,
  system_instruction=(
  "You are a friendly, creative assistant whose name is Jarvis who gives short, fun facts about any topic the user asks. Keep answers under 50 words."

)
)

def speak_old(text):# this function speaks the text 
    engine = pyttsx3.init() # Initilize pyttsx module
    print(f"{text}")
    # engine.say("hello sir")
    engine.say(text) # Queues the text you want the speech engine to say.
    engine.runAndWait()#  Tells the engine to process and speak everything that was queued

def speak(text):
  tts = gTTS(text)
  tts.save("temp.mp3")

  
  # Initialize pygame mixer
  pygame.init()
  pygame.mixer.init()

  # Load your MP3 file
  pygame.mixer.music.load("temp.mp3")  # Replace with your file path

  # Play the music
  pygame.mixer.music.play()

  # Optional: Keep the script alive while the music plays
  while pygame.mixer.music.get_busy():
      time.sleep(1)
     
  pygame.mixer.music.unload()    
  os.remove("temp.mp3") 
def ask_gemini(c): # handel the request of the user input
    try:
        response = model.generate_content(c) # process the user input to the model 
        return response.text  # return the content that model generated 
    except Exception as e:
        return f"Error: {str(e)}"
      
def processCommand(c):
    d = c.lower() 
    print(d)
    
      
    if d == "open youtube":
     webbrowser.open("https://www.youtube.com") 
    elif d == "open google":
      webbrowser.open("https://www.google.com")    
    elif d == "open facebook":
      webbrowser.open("https://www.facebook.com")    
    elif d == "open linkedin":
      webbrowser.open("https://www.linkedin.com")    
    elif d == "open reddit":
      webbrowser.open("https://www.reddit.com")    
    elif d == "open instagram":
      webbrowser.open("https://www.instagram.com")    
    elif d.startswith("play"):
     try:
        song = d.split(" ")[1]
        link = music_library.music[song]
        # print(link)
        webbrowser.open(link)
        speak(f"Playing {song}")
        exit()
     except KeyError:
        speak(f"Sorry, I couldn't find {song} in your music library.") 
        
    elif "news" in d:

        #  URL to fetch news from
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}"

        # Make the HTTP request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract the articles
            articles = data.get("articles", [])
            
            # Speak the headlines
            for _,article in enumerate(articles[:10],5):          
             speak(f"{article['title']}")
            
    
    elif d == "exit":
        speak("bye bye sir ...")
        exit()  
    
    else:
      output = ask_gemini(command)
      speak(output)
     #  handle the request to Google gemnini
        
        

if __name__ == "__main__":
     speak("Initializing jarvis......")
    
        # Listen for the wake word "jarvis"
        # obtain audio from the microphone
        # tried sphinx but not so good
        # used recognize_google insted of recognize_sphinx
     r = sr.Recognizer()
     try:
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source,phrase_time_limit = 5)
            print("recognizing")
            word = r.recognize_google(audio)

            if(word.lower() == "jarvis"): 
               speak("hello sir, How can i help you today?")
            # Listen for Command
            while True: 
               with sr.Microphone() as source:
                  print("Jarvis Active.....")
                  audio = r.listen(source)
                  command = r.recognize_google(audio)
                  processCommand(command)
                                                    
     except sr.UnknownValueError:
            print("J.A.R.V.I.S could not understand audio")
     except sr.RequestError as e:
            print("J.A.R.V.I.S error; {0}".format(e))

 
 
 