# // prompt_service.py

from models import Setting, PromptQuestion, Prompt
from security import decrypt_api_key
from sqlmodel import Session, select
from services.ai_service import generate_initial_questions, generate_final_outputs

async def create_prompt_session(
        session: Session,
        user_input: str,
        domain: str,
        knowledge_level: str,
        wants_turkish_response: bool = False
) -> Prompt:
    setting = session.exec(select(Setting).where(Setting.id ==1)).first()
    if not  setting:
        raise ValueError("Settings not configured yed.")

    if setting.active_provider == "gemini":
        encrypted_key = setting.gemini_api_key_encrypted
    else:
        encrypted_key = setting.openrouter_api_key_encrypted

    if not encrypted_key:
        raise ValueError(f"API Key for {setting.active_provider} is missing")

    api_key = decrypt_api_key(encrypted_key)

    questions = await generate_initial_questions(
        raw_idea=user_input,
        domain=domain,
        knowledge_level=knowledge_level,
        provider=setting.active_provider,
        model_name=setting.preferred_model,
        api_key=api_key
    )
    new_prompt = Prompt(
        user_input=user_input,
        domain=domain,
        knowledge_level=knowledge_level,
        wants_turkish_response=wants_turkish_response,
        ai_model_used=setting.preferred_model,
        status="QUESTIONING"
    )

    session.add(new_prompt)
    session.commit()
    session.refresh(new_prompt)

    for idx, q_text in enumerate(questions, start=1):
        questions_obj = PromptQuestion(
            prompt_id=new_prompt.id,
            question=q_text,
            order_index=idx
        )
        session.add(questions_obj)

    session.commit()
    session.refresh(new_prompt)
    return new_prompt

async def submit_answers_and_generate_final(
        session: Session,
        prompt_id: str,
        user_answers: dict[str, str],
) -> Prompt:
    prompt = session.get(Prompt, prompt_id)
    if not prompt: raise ValueError(f"Prompt with id {prompt_id} not found.")

    qa_pairs = []
    for q in prompt.questions:
        if q.id in user_answers:
            q.user_answer = user_answers[q.id]
            session.add(q)
        qa_pairs.append({"question": q.question, "answer": q.user_answer or ""})

    setting = session.exec(select(Setting).where(Setting.id == 1)).first()
    if not setting:
        raise ValueError("Settings not congigured yet.")
    if setting.active_provider == "gemini":
        encrypted_key = setting.gemini_api_key_encrypted
    else:
        encrypted_key = setting.openrouter_api_key_encrypted
    if not encrypted_key:
            raise ValueError(f"API Key for {setting.active_provider} is missing.")
    
    api_key = decrypt_api_key(encrypted_key)

    final_data = await generate_final_outputs(
        raw_idea=prompt.user_input,
        domain=prompt.domain,
        knowledge_level=prompt.knowledge_level,
        qa_pairs=qa_pairs,
        model_name=prompt.ai_model_used,
        provider=setting.active_provider,
        api_key=api_key,
        wants_turkish_response=prompt.wants_turkish_response
    )

    prompt.english_prompt = final_data["english_prompt"]
    prompt.turkish_translation = final_data["turkish_translation"]
    prompt.turkish_explanation = final_data["turkish_explanation"]
    prompt.status = "COMPLETED"

    session.add(prompt)
    session.commit()
    session.refresh(prompt)
    return prompt