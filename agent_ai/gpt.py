from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set API key for OpenAI client
api_key = os.getenv("API_KEY")
openai.api_key = api_key  # Set the API key directly in openai module

txt_file_path = "database/knowledge_base.txt"

# Function to read the text file
def read_txt_file(txt_file_path):
    with open(txt_file_path, 'r') as file:
        return file.read()

knowledge_base_content = read_txt_file(txt_file_path)

def generate_response(user_message: str) -> str:
    # Create the prompt messages for the chat model
    messages = [
        {"role": "system", "content": knowledge_base_content},  # Use your knowledge base content as a system message
        {"role": "user", "content": user_message}  # The user's message
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",  # Change as required
        messages=messages,
        max_tokens=150,
        temperature=0.7,
    )

    # Extract the assistant's response from the API response
    ai_response = response['choices'][0]['message']['content'].strip()

    # Create a Twilio response object
    twilio_response = MessagingResponse()
    twilio_response.message(ai_response)
    response_content = str(twilio_response)

    return response_content
