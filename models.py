# // models.py

from sqlmodel import Field, SQLModel, JSON, Column, Relationship
import uuid
from datetime import datetime, timezone

class Prompt(SQLModel, table=True):

    __tablename__ = "prompts"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        max_length=36,
        )
    domain: str = Field(max_length=100)
    domain_options: dict | None = Field(default=None, sa_column=Column(JSON))
    knowledge_level: str = Field(max_length=20)
    global_system_prompt: str |None = Field(default=None)

    user_input: str | None = Field(default=None)
    english_prompt: str | None = Field(default=None)
    turkish_translation: str | None = Field(default=None)
    turkish_explanation: str | None = Field(default=None)

    wants_turkish_response: bool = Field(default=False)

    ai_model_used: str = Field(max_length=50)

    status: str = Field(default="DRAFT", max_length=20)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None,sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},)
    questions: list["PromptQuestion"] = Relationship(back_populates="prompt")

class PromptQuestion(SQLModel, table=True):

    __tablename__ = "prompt_questions"

    id: str = Field(
            default_factory=lambda: str(uuid.uuid4()),
            primary_key=True,
            max_length=36,
            )
    
    prompt_id: str = Field(foreign_key="prompts.id", max_length=36)
    question: str
    user_answer: str | None = Field(default=None)
    order_index: int = Field(default=1)
    is_skipped: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prompt: Prompt | None = Relationship(back_populates="questions")

class Setting(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    gemini_api_key_encrypted: str | None = Field(default=None)
    openrouter_api_key_encrypted: str | None = Field(default=None)

    active_provider: str = Field(default="gemini")
    preferred_model: str = Field(default="gemini-3.1-flash-lite")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None,sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},)