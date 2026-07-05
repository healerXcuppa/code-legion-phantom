#Creating Free Trial ChatBot with a free google genai API Key
import os
import time
import shutil
from dotenv import load_dotenv
from  google  import genai

#Loads the API key in the environment file
load_dotenv()

# Uses the shutil import to align and center objects
width = shutil.get_terminal_size().columns

# Using the API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# CHATBOT INTRO AFTER SCREEN CLEAR
def clear_screen():
    """Clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
clear_screen()
    
print()
print(f"{'='*width}")
print("healerXcuppa AI ASSISTANT".center(width))
print(f"{'='*width}")
print()

# Model to be used and the where questions are sent
chat = client.chats.create(
    model="gemini-2.5-flash"
)

while True:
    
    # Asking my question
    my_question = input("You: ")
    
    # Exiting the program
    if my_question.lower() == "exit":
        time.sleep(2)
        print("Exiting the chatbot. Goodbye!")
        time.sleep(2)
        clear_screen()
        break
    
    if not my_question.strip():
        print("Please type something.\n")
        continue
    
    # Using response to answer my questions
    response = chat.send_message(my_question)

    print(f"Bot: {response.text}")
    print()