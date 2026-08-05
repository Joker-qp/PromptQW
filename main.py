from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from database import create_db_and_tables, get_session
from security import encrypt_api_key
from sqlmodel import Session, select
from pydantic import BaseModel
from models import Setting, Prompt
from services.prompt_service import (create_prompt_session, submit_answers_and_generate_final)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Interactive Prompt Architect API",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
async def root():
    return {"status": "healthy", "message": "Interactive Prompt Arcitect API is running"}

class SettingUpdate(BaseModel):
    gemini_api_key: str | None = None
    openrouter_api_key: str | None = None
    active_provider: str = "gemini"
    preferred_model: str = "gemini-3.1-flash-lite"

class SettingResponse(BaseModel):
    active_provider: str
    preferred_model: str
    has_gemini_key: bool
    has_openrouter_key: bool

@app.post("/api/settings", response_model=SettingResponse)
async def update_settings(
    data: SettingUpdate,
    session: Session = Depends(get_session)
):
    setting = session.exec(select(Setting).where(Setting.id == 1)).first()
    if not setting:
        setting = Setting(id=1)

    if data.gemini_api_key:
        setting.gemini_api_key_encrypted = encrypt_api_key(data.gemini_api_key)
    if data.openrouter_api_key:
        setting.openrouter_api_key_encrypted = encrypt_api_key(data.openrouter_api_key)

    setting.active_provider = data.active_provider
    setting.preferred_model = data.preferred_model

    session.add(setting)
    session.commit()
    session.refresh(setting)

    return SettingResponse(
        active_provider=setting.active_provider,
        preferred_model=setting.preferred_model,
        has_gemini_key=bool(setting.gemini_api_key_encrypted),
        has_openrouter_key=bool(setting.openrouter_api_key_encrypted)
    )

@app.get("/api/settings", response_model=SettingResponse)
async def get_settings(session: Session = Depends(get_session)):
    setting = session.exec(select(Setting).where(Setting.id == 1)).first()
    if not setting:
        return SettingResponse(
            active_provider="gemini",
            preferred_model="gemini-3.1-flash-lite",
            has_gemini_key=False,
            has_openrouter_key=False
        )
    return SettingResponse(
        active_provider=setting.active_provider,
        preferred_model=setting.preferred_model,
        has_gemini_key=bool(setting.gemini_api_key_encrypted),
        has_openrouter_key=bool(setting.openrouter_api_key_encrypted)
    )

class PromptCreate(BaseModel):
    user_input: str
    domain: str
    knowledge_level: str
    wants_turkish_response: bool = False

class PromptAnswerSubmit(BaseModel):
    answers: dict[str, str]

@app.post("/api/prompts")
async def start_prompt_session(
    data: PromptCreate,
    session: Session = Depends(get_session)
):
    try:
        new_prompt = await create_prompt_session(
            session=session,
            user_input=data.user_input,
            domain=data.domain,
            knowledge_level=data.knowledge_level,
            wants_turkish_response=data.wants_turkish_response
        )
        return {"prompt": new_prompt, "questions": new_prompt.questions}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/prompts/{prompt_id}/answers")
async def submit_prompt_answers(
    prompt_id: str,
    data: PromptAnswerSubmit,
    session: Session = Depends(get_session)
):
    try:
        update_prompt = await submit_answers_and_generate_final(
            session=session,
            prompt_id=prompt_id,
            user_answers=data.answers
        )
        return update_prompt
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/prompts")
async def list_prompts(sesion: Session = Depends(get_session)):
    prompts = sesion.exec(select(Prompt).order_by(Prompt.created_at.desc())).all()
    return prompts

@app.get("/api/prompts/{prompt_id}")
async def get_prompt_detail(prompt_id: str, session: Session = Depends(get_session)):
    prompt = session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt
