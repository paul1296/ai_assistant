from agent_ai.models.models import *
from agent_ai.models.database import *
from agent_ai.crud.crud import *
import uuid

# Define a namespace for generating UUIDs (can be any UUID)
NAMESPACE = uuid.UUID('12345678-1234-5678-1234-567812345678')
db = get_db()

def generate_conversation_history(sender: str):
    user_id = uuid.uuid5(NAMESPACE, sender)
    user = get_user(db=db, user_id=user_id)
    messages = get_messages_for_today(db=db, user_id=user.internal_id)
    context = []

    for message in messages:
        reply = get_replies(db=db, message_id=message.internal_id, user_id=user_id)
        context.append({"role": "user", "content": message}, {"role": "assistant", "content": reply})

    return context