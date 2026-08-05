# // database.py

from sqlmodel import create_engine, Session, SQLModel
from models import Prompt, PromptQuestion, Setting

engine = create_engine("sqlite:///PromptQW_database.db", connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session