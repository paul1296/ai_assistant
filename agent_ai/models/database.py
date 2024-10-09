from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException

SQLALCHEMY_DATABASE = "sqlite:///conversations.db"

engine = create_engine(SQLALCHEMY_DATABASE, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Yield the session, for use in request handling
    finally:
        db.close()  # Close the session when the request is done