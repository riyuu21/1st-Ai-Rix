# libraries used
from groq import Groq
from json import load,dump
import datetime
from dotenv import dotenv_values

# API
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIkey = env_vars.get("GroqAPIkey")
client = Groq(api_key=GroqAPIkey)

# user messages
messages = []

# System message that provides context to dear Rix
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# System instructions to chatbot
SystemChatBot = [ 
    {"role" : "system", "content" : System}
]

# Chat log in a file
try : 
    # load existing messages of json file
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    # if no json file exist create a new empty one
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to get real-time date and time info
def RealtimeInformation():
    # get current date and time
    Current_date_time = datetime.datetime.now()
    day = Current_date_time.strftime("%A")
    date = Current_date_time.strftime("%d")
    month = Current_date_time.strftime("%B")
    year = Current_date_time.strftime("%Y")
    hour = Current_date_time.strftime("%H")
    minute = Current_date_time.strftime("%M")
    second = Current_date_time.strftime("%S")

    # For a string format
    data = f"Please use this real-time information if needed,\n"
    data += f"Day : {day}\nDate : {date}\nMonth : {month}\nYear : {year}\n"
    data += f"Time : {hour} hours : {minute} minutes : {second} seconds.\n"
    return data

# Function to modify response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split('\n') # Split the response into lines
    non_empty_lines = [line for line in lines if line.strip()] # Remove empty lines
    modified_answer = '\n'.join(non_empty_lines) # join cleaned lines back together
    return modified_answer

# Main Chatbot that handles user queries
def ChatBot(Query):
    """ This function sends the user's query to chatbot and returns AI's response. """

    try:
        # Load the existing chat from earlier made json file
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
        
        # Append(add) user's query to the messages list.
        messages.append({"role" : "user", "content" : f"{Query}"})

        # Make a req to groq for a response.
        Completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=SystemChatBot + [{"role" : "system", "content" : RealtimeInformation()}] + messages, # Include sys instructions, real-time info and chat mastery.
            max_tokens=1024, # Limit no. of max tokens in a response.
            temperature=0.7, # this is directly proportional to randomness
            top_p=1, # Use nucleus sampling to control diversity.
            stream=True, # Enable streaming response 
            stop=None # Allow model to determine when to stop
        )

        Answer = "" # Initialize empty string to store AI's response.

        # Process the streamed response chunks.
        for chunk in Completion:
            if chunk.choices[0].delta.content: # Check if there's content in current chunk
                Answer += chunk.choices[0].delta.content # append the content to answer

        Answer = Answer.replace("</s>", "") # clean any unwanted tokens from the response.

        # Append the chatbot's response to the messages list.
        messages.append({"role" : "assistant", "content" : Answer})

        # Save the updated chat log in json file.
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        # Return the formatted response.
        return AnswerModifier(Answer=Answer)
    
    except Exception as e:
        # Handle errors by printing the exception and resetting the chat log.
        print(f"Error : {e}")
        with open (r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return "Something went wrong. Please check your API key or internet connection." # Retry the query after resetting the log.
    
# Main program entry point.
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question : ") # prompt the user for a question.
        print(ChatBot(user_input)) # Call the chatbot function and print its response.