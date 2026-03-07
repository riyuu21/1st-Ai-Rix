# req libs
from AppOpener import close,open as appopen # To close open apps 
from webbrowser import open as webopen # web browser functionality
from pywhatkit import search, playonyt # for google search and youtube playback
from dotenv import dotenv_values # to manage environment variables
from bs4 import BeautifulSoup # for html content
from rich import print # for styles console output
from groq import Groq # for groq
import webbrowser # to open url's
import subprocess # to interact with system
import requests # to make html req
import keyboard # for keyboard related actions
import asyncio # for asynchronous programming
import os # for os functionalities

# API key
env_vars = dotenv_values(".env")
CohereAPIkey = env_vars.get("CohereAPIkey")
GroqAPIkey = env_vars.get("GroqAPIkey")

# Define CSS classes for parsing specific elements in html content
classes = ["zCubwf" ,"hgKElc" ,"LTKOO sY7ric" ,"ZOLcW",
"gsrt vk_bk FzvWSb YwPhnf","pclqee","qv3wpe","kno-rdesc","SPZz6b"
"tw-Data-text tw-text-small tw-ta","Iz6rdc","O5uR6d LTKOO",
"vlzV6d","webanswers-webanswers_table__webanswers-table",
"dDoNo ikb4Bb gsrt","sxLAoe","LwKfke","VQF4g",]

# Define a user-agent to make web requests
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with API key
client = Groq(api_key=GroqAPIkey)

# Predefined professional responses for user interactions
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

# List to store chatbot messages
messages = []

# to provide context to the chatbot
SystemChatBot = [{"role" : "system", "content" : f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# Function to perform a google search
def GoogleSearch(Topic):
    search(Topic) # use pywhatkit's search function to perform a google search
    return True

# Function to generate content using AI and save it
def Content(Topic):
    # Nested function to open a file in notepad.
    def OpenNotepad(file):
        default_text_editor = 'notepad.exe' # Default
        subprocess.Popen({default_text_editor, file}) # Open a file in Notepad

        # Nested function to generate content using the AI chatbot
        def ContentWriterAI(prompt):
            messages.append({"role" : "user", "content" : f"{prompt}"}) # Add user's prompt to messages

            completion = client.chat.completions.create( 
                model='mixtral-8x7b-32768', # AI model
                messages=SystemChatBot + messages, # Include sys instructions in chat history
                 max_tokens=2048 # Limit the maximum tokens in response
            )