from pydantic import BaseModel

# Define the Message model
class Message(BaseModel):
    Body: str