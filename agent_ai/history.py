from agent_ai.models.models import *
from agent_ai.models.database import *
from agent_ai.crud.crud import *
import uuid

# Define a namespace for generating UUIDs (can be any UUID)
NAMESPACE = uuid.UUID('12345678-1234-5678-1234-567812345678')

def generate_conversation_history(sender: str, db):
    user_id = str(uuid.uuid5(NAMESPACE, sender))
    user = get_user(db=db, user_id=user_id)
    messages = get_messages_for_today(db=db, user_id=user.internal_id)
    context = []

    for message in messages:
        # Extract the text from the message
        message_content = message.text if message else ""  # Ensure message exists
        reply = get_replies(db=db, message_id=message.internal_id, user_id=user_id)
        
        # Extract the text from the reply as well
        reply_content = reply.text if reply else ""  # Ensure reply exists

        # Append only the text content to the context
        context.extend([
            {"role": "user", "content": message_content},
            {"role": "assistant", "content": reply_content}
        ])

    return context
