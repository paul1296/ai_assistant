
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key=os.getenv("API_KEY")

client = OpenAI(api_key=api_key)
txt_file_path = "database/knowledge_base.txt"

# Function to read the text file
def read_txt_file(txt_file_path):
    with open(txt_file_path, 'r') as file:
        return file.read()

knowledge_base_content = read_txt_file(txt_file_path)

def generate_response(message: str) -> str:

    # Get a response from OpenAI
    prompt = f"{knowledge_base_content}\nUser: {user_message}\nAI:"
    response = client.completions.create(engine="gpt-4",
    prompt=prompt,
    max_tokens=150,
    n=1,
    stop=None,
    temperature=0.7)
    ai_response = response.choices[0].text.strip()
    # Create a Twilio response object
    twilio_response = MessagingResponse()
    twilio_response.message(ai_response)
    response_content = str(twilio_response)

    return response_content