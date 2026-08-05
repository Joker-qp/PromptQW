# // ai_service.py
import os
from google import genai 
from google.genai import types
import httpx
import json

async def generate_llm_response(
        provider: str,
        model_name: str,
        api_key: str,
        system_prompt: str,
        user_prompt: str
) -> str:
    try:
        if provider == "gemini":
            client = genai.Client(api_key=api_key)
            config = types.GenerateContentConfig(system_instruction=system_prompt)
            response = await client.aio.models.generate_content(
                model=model_name,
                contents=types.Part.from_text(text=user_prompt),
                config=config
            )
            return response.text
        elif provider == "openrouter":
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    except Exception as e:
        raise RuntimeError(f"AI Servisi ({provider}) geçici olarak yanıt vermiyor. Lütfen tekrar deneyin: {e}")    

async def generate_initial_questions(
        raw_idea: str,
        domain: str,
        knowledge_level: str,
        provider: str,
        model_name: str,
        api_key: str
    ) -> list[str]:
    system_prompt = (
    "You are an expert Prompt Architect. Analyze the user's idea, domain, and knowledge level. "
    "Generate between 3 and 10 highly relevant, targeted questions to mature and deeply understand their goal. "
    "CRITICAL: Your output MUST be ONLY a valid JSON array of strings, like this: "
    '["Question 1?", "Question 2?", "Question 3?"]. '
    "Do NOT wrap it in markdown code blocks, do NOT write any intro/outro text."
)
    user_prompt = f"Idea: {raw_idea}\nDomain: {domain}\nKnowledge_level: {knowledge_level}"

    raw_response = await generate_llm_response(provider, model_name, api_key, system_prompt, user_prompt)
    cleaned_response = raw_response.strip()
    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.split("\n", 1)[-1].rsplit("\n", 1)[0].strip()
    questions = json.loads(cleaned_response)
    return questions


async def generate_final_outputs(
        raw_idea: str,
        domain: str,
        knowledge_level: str,
        qa_pairs: list[dict],
        provider: str,
        model_name: str,
        api_key: str,
        wants_turkish_response: bool = False
) -> dict:
    system_prompt = (
    "You are a World-Class Prompt Engineer. Your task is to analyze the user's initial idea and their answers to refining questions, "
    "then generate 3 specific outputs in JSON format:\n"
    "1. 'english_prompt': A highly structured, professional English prompt following Role, Context, Task, Constraints, and Output Format standards.\n"
    "2. 'turkish_translation': An exact, high-quality Turkish translation of the final English prompt.\n"
    "3. 'turkish_explanation': A clear, educational guide in Turkish explaining how this prompt was constructed and how to use it, tailored to the user's knowledge level.\n\n"
    "CRITICAL: Output ONLY a valid JSON object with EXACTLY these 3 keys: 'english_prompt', 'turkish_translation', 'turkish_explanation'. "
    "Do NOT wrap it in markdown backticks or extra text."
    )

    formatted_qa = "\n".join([f"Q: {q.get('question')}\nA: {q.get('answer')}" for q in qa_pairs])

    user_prompt = (
    f"Initial Idea: {raw_idea}\n"
    f"Domain: {domain}\n"
    f"Target Knowledge Level: {knowledge_level}\n"
    f"Refining Questions & Answers:\n{formatted_qa}\n"
    f"User wants final response guidance in Turkish: {wants_turkish_response}"
    )
    raw_response = await generate_llm_response(provider, model_name, api_key, system_prompt, user_prompt)
    cleaned_response = raw_response.strip()
    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.split("\n", 1)[-1].rsplit("\n", 1)[0].strip()
    final_prompt = json.loads(cleaned_response)
    return final_prompt

