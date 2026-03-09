# req libs
from AppOpener import close, open as appopen  # To close/open apps
from webbrowser import open as webopen        # Web browser functionality
from pywhatkit import search, playonyt        # For Google search and YouTube playback
from dotenv import dotenv_values              # To manage environment variables
from bs4 import BeautifulSoup                 # For HTML content parsing
from rich import print                        # For styled console output
from groq import Groq                         # For Groq API
import webbrowser                            # To open URLs
import subprocess                            # To interact with system
import requests                              # To make HTTP requests
import keyboard                              # For keyboard related actions
import asyncio                               # For asynchronous programming
import os                                    # For OS functionalities
from concurrent.futures import ThreadPoolExecutor

# API key
env_vars = dotenv_values(".env")
GroqAPIkey = env_vars.get("GroqAPIkey")

# Define CSS classes for parsing specific elements in HTML content
classes = [
    "zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf",
    "pclqee", "qv3wpe", "kno-rdesc", "SPZz6b", "tw-Data-text tw-text-small tw-ta",
    "Iz6rdc", "O5uR6d LTKOO", "vlzV6d", "webanswers-webanswers_table__webanswers-table",
    "dDoNo ikb4Bb gsrt", "sxLAoe", "LwKfke", "VQF4g",
]

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

# To provide context to the chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# Thread pool for faster execution of blocking tasks
executor = ThreadPoolExecutor(max_workers=10)

# Cache for Google search results
search_cache = {}

# Function to perform a Google search
def GoogleSearch(Topic):
    search(Topic)  # Use pywhatkit's search function to perform a Google search
    return True

# Function to generate content using AI
def ContentWriterAI(prompt):
    messages.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model='mixtral-8x7b-32768',
        messages=SystemChatBot + messages,
        max_tokens=2048,
        temperature=0.5,
        top_p=1,
        stream=True,
        stop=None
    )
    Answer = ''
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    Answer = Answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    return Answer

def OpenNotepad(file):
    default_text_editor = 'notepad.exe'
    subprocess.Popen([default_text_editor, file], start_new_session=True)  # Non-blocking

def Content(Topic):
    Topic = Topic.replace("content ", "")
    ContentByAI = ContentWriterAI(Topic)
    filename = rf"Data\{Topic.lower().replace(' ', '')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
    OpenNotepad(filename)
    return True

def YoutubeSearch(Topic):
    url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_lines(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            if query in search_cache:
                return search_cache[query]
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                search_cache[query] = response.text
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None

        html = search_google(app)
        if html:
            link = extract_lines(html)[0]
            webopen(link)
        return True

def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    def mute(): keyboard.press_and_release("volume mute")
    def unmute(): keyboard.press_and_release("volume mute")
    def volume_up(): keyboard.press_and_release("volume up")
    def volume_down(): keyboard.press_and_release("volume down")

    if command == "mute": mute()
    elif command == "unmute": unmute()
    elif command == "volume up": volume_up()
    elif command == "volume down": volume_down()
    return True

# Asynchronous function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            funcs.append(asyncio.get_event_loop().run_in_executor(executor, OpenApp, command.removeprefix("open ")))
        elif command.startswith("Close "):
            funcs.append(asyncio.get_event_loop().run_in_executor(executor, CloseApp, command.removeprefix("close ")))
        elif command.startswith("Play "):
            funcs.append(asyncio.get_event_loop().run_in_executor(executor, PlayYoutube, command.removeprefix("play ")))
        elif command.startswith("Content "):
            funcs.append(asyncio.get_event_loop().run_in_executor(executor, Content, command.removeprefix("Content ")))
        elif command.startswith("Google search "):
            funcs.append(asyncio.get_event_loop().run_in_executor(executor, GoogleSearch, command.removeprefix("Google search ")))
        elif command.startswith("youtube search"):
            funcs.append(asyncio.get_event_loop().run_in_executor(executor, YoutubeSearch, command.removeprefix("youtube search")))
        elif command.startswith("system "):
            funcs.append(asyncio.get_event_loop().run_in_executor(executor, System, command.removeprefix("system ")))
        else:
            print(f"No Function Found for {command}")

    # Run all tasks in parallel
    results = await asyncio.gather(*funcs, return_exceptions=True)
    return results

# Asynchronous function to automate command execution
async def Automation(commands: list[str]):
    results = await TranslateAndExecute(commands)
    for result in results:
        pass
    return True

if __name__ == "__main__":
    asyncio.run(Automation(["open instagram", "Play despacito", "Google search AI"]))
