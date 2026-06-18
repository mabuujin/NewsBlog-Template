from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

url = os.getenv("DATABASE_URL")
engine = create_engine(url)

def get_session():
    return Session(engine)