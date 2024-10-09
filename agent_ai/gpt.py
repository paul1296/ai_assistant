from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv
import os
from . import history
from agent_ai.crud.crud import *
from agent_ai.models.database import *


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
    user_id = str(uuid.uuid5(NAMESPACE, sender))
    user = get_user(db=db, user_id=user_id)
    print(user_id)
    # If user does not exist, create one
    if user is None:
        user = create_user(whatsapp=sender, db=db)  # Pass db to create_user

    context = history.generate_conversation_history(sender=sender, db=db)  # Pass db to history function
    messages.extend(context)
    messages.append({"role": "user", "content": user_message})  # The user's message
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",  # Change as required
        messages=messages,
        max_tokens=150,
        temperature=0.7,
    )

    # Extract the assistant's response from the API response
    ai_response = response['choices'][0]['message']['content'].strip()
    new_message = create_message(db=db, internal_user_id=user.internal_id, text=user_message)
    create_reply(db=db, internal_user_id=user.internal_id, internal_message_id=new_message.internal_id, text=ai_response)

    # Create a Twilio response object
    twilio_response = MessagingResponse()
    twilio_response.message(ai_response)
    response_content = str(twilio_response)

    return response_content
