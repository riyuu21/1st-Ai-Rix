# Libraries req.
from googlesearch import search
from groq import Groq # groq lib to use its api
from json import load, dump # to read write json files
import datetime # for real time date and time info
from dotenv import dotenv_values # to read .env file

# Load env file
env_vars = dotenv_values(".env")

# Retrieve environment variables for chatbot
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIkey = env_vars.get("GroqAPIkey")

# Initialize the Groq client with provided api key.
client = Groq(api_key=GroqAPIkey)

# Define the sys instrctions for the chatbot (prompt).
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to loadd the chat log from json file or just create one.
try:
    with open (r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open (r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Search google and format the result using a function.
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"Search results for '{query}':\n\n"

    for i in results:
        Answer += f"Title: {i.title}\n"
        Answer += f"Description: {i.description}\n"
        Answer += f"URL: {i.url}\n\n"

    return Answer

# Function to clean up the answer.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [ 
    {"role" : "system", "content" : System},
    {"role" : "user", "content" : "Hi"},
    {"role" : "assistant", "content" : "Hello, how can i help you?"}
]

# Function to get real time information like the current date and time.
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    # For a string format
    data = f"Please use this real-time information if needed,\n"
    data += f"Day : {day}\nDate : {date}\nMonth : {month}\nYear : {year}\n"
    data += f"Time : {hour} hours : {minute} minutes : {second} seconds.\n"
    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load the chat log from json file.
    with open (r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role" : "user", "content" : f"{prompt}"})

    # Add Google search results as assistant context
    search_results = GoogleSearch(prompt)
    messages.append({"role": "assistant", "content": search_results})

    # Add real-time info as assistant context
    messages.append({"role": "assistant", "content": Information()})

    # Generate a response using groq.
    completion = client.chat.completions.create ( 
        model="llama-3.1-8b-instant",
        messages = SystemChatBot + messages[-8:], # include system + last 8 turns
        max_tokens=1024,
        temperature=0.2, # lower for factual consistency
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = "" # Initialize empty string to store AI's response.

    # Process the streamed response chunks.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")

    # Append the chatbot's response to the messages list.
    messages.append({"role" : "assistant", "content" : Answer})

    # Save the updated chat log in json file.
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)  

    return AnswerModifier(Answer=Answer)

# Main program entry point.
if __name__ == "__main__":
    while True:
        prompt = input("Enter Your Query : ")
        print(RealtimeSearchEngine(prompt))
