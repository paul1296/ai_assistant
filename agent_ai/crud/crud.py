from agent_ai.models import models
import uuid
from sqlalchemy.orm import Session


# Define a namespace for generating UUIDs (can be any UUID)
NAMESPACE = uuid.UUID('12345678-1234-5678-1234-567812345678')

def get_user(db:Session, user_id: str):
    return db.query(models.User).filter(models.User.internal_id == user_id).first()

def get_message(db:Session, message_id: str):
    return db.query(models.Message).filter(models.User.internal_id == message_id).first()

def get_reply(db:Session, reply_id: str):
    return db.query(models.Reply).filter(models.Reply.internal_id == reply_id).first()

def create_user(db:Session, whatsapp: str):
    db_user = models.User(internal_id=uuid.uuid5(NAMESPACE, whatsapp), whatsapp=whatsapp)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_message(db:Session, internal_user_id: str, text: str):
    db_message = models.Message(internal_id=uuid.uuid4(), internal_user_id=internal_user_id,text=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def create_reply(db:Session,internal_user_id: str, internal_message_id:str, text: str):
    db_reply = models.Message(internal_id=uuid.uuid4(), internal_user_id=internal_user_id, internal_message_id=internal_message_id, text=text)
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return db_reply

def update_reply(db: Session, reply_id: str, text: str = None):
    db_reply = get_reply(db, reply_id)
    if db_reply:
        if text is not None:
            db_reply.text = text
        db.commit()
        db.refresh(db_reply)
        return db_reply
    return None

def update_user(db: Session, user_id: str, whatsapp: str = None, active: bool = None):
    db_user = get_user(db, user_id)
    if db_user:
        if whatsapp is not None:
            db_user.whatsapp = whatsapp
        if active is not None:
            db_user.active = active
        db.commit()
        db.refresh(db_user)
        return db_user
    return None