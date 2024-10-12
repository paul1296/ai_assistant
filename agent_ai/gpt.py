from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv
import os
from . import history
from agent_ai.crud.crud import *
from agent_ai.models.database import *
import json


# Load environment variables from .env file
load_dotenv()

# Set API key for OpenAI client
api_key = os.getenv("API_KEY")
openai.api_key = api_key  # Set the API key directly in openai module

txt_file_path = "agent_ai/database/knowledge_base.txt"

# Function to read the text file
def read_txt_file(txt_file_path):
    with open(txt_file_path, 'r') as file:
        return file.read()

knowledge_base_content = read_txt_file(txt_file_path)

def generate_response(user_message: str, sender: str, db: Session) -> str:
    # Create the prompt messages for the chat model
    messages = [{"role": "system", "content": knowledge_base_content}]  # Use your knowledge base content as a system message   
    fine_tune_data = load_jsonl(file_path="agent_ai/fine_tune_data.jsonl")

    for data in fine_tune_data:   
        messages.extend(data["messages"])

    user_id = str(uuid.uuid5(NAMESPACE, sender))
    user = get_user(db=db, user_id=user_id)
    # If user does not exist, create one
    if user is None:
        user = create_user(whatsapp=sender, db=db)  # Pass db to create_user

    context = history.generate_conversation_history(user_id=user.internal_id, db=db)  # Pass db to history function
    messages.extend(context)
    new_message = create_message(db=db, internal_user_id=user.internal_id, text=user_message)
    messages.extend([{"role": "user", "content": new_message.text}])  # The user's message
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use your fine-tuned model
        messages=messages,
        max_tokens=200,
        temperature=0.7,
    )

    # Extract the assistant's response from the API response
    ai_response = response['choices'][0]['message']['content'].strip()
    reply = create_reply(db=db, internal_user_id=user.internal_id, internal_message_id=new_message.internal_id, text=ai_response)

    # Create a Twilio response object
    twilio_response = MessagingResponse()
    twilio_response.message(ai_response)
    response_content = str(twilio_response)

    return response_content

# Function to load a JSONL file into a list
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Strip whitespace and load the JSON object from each line
            json_object = json.loads(line.strip())
            data.append(json_object)
    return data
