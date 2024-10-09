from sqlalchemy import create_engine, MetaData, Table, Column, String, ForeignKey, Boolean, Text, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

# Base class for ORM models
Base = declarative_base()

# Define the User, Message, and Reply classes (based on the tables)
class User(Base):
    __tablename__ = 'user'
    internal_id = Column(String, primary_key=True)
    whatsapp = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.timezone.utcnow)
    deleted_at = Column(DateTime,  nullable=True)
    active = Column(Boolean, nullable=False, default=True)

class Message(Base):
    __tablename__ = 'message'
    internal_id = Column(String, primary_key=True)
    internal_user_id = Column(String, ForeignKey('user.internal_id'))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.timezone.utcnow)

class Reply(Base):
    __tablename__ = 'reply'
    internal_id = Column(String, primary_key=True)
    internal_user_id = Column(String, ForeignKey('user.internal_id'))
    internal_message_id = Column(String, ForeignKey('message.internal_id'))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.timezone.utcnow)