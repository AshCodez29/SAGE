import os

from openai import OpenAI

client = None
model_name = None

SYSTEM_PROMPT = """
You are SAGE - a personal AI assistant running on the user's laptop.
You are intelligent, calm, and slightly witty. Like JARVIS but smarter.

Rules:
- Keep responses SHORT - max 2-3 sentences unless asked for more
- Match the user's language: Hindi -> reply Hindi, Hinglish -> reply Hinglish
- You can use casual words like 'yaar', 'bhai', 'theek hai' naturally
- Never say you're an AI model - you are SAGE
- If the user seems frustrated, be direct. If excited, match their energy.
"""

conversation_history = []


def _get_llm_client():
    api_key = os.getenv("GROQ_API") or os.getenv("GROQ_API_KEY")
    if api_key:
        return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1"), "llama-3.3-70b-versatile"

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return OpenAI(api_key=api_key), "gpt-4o"

    raise RuntimeError("Missing API key. Set GROQ_API or OPENAI_API_KEY in your environment or .env file.")


def think(user_input: str) -> str:
    global client, model_name
    if client is None:
        client, model_name = _get_llm_client()

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *conversation_history],
        max_tokens=150,
    )

    reply = response.choices[0].message.content.strip()

    conversation_history.append({"role": "assistant", "content": reply})

    # Keep only the last 10 turns (20 messages: user+assistant pairs).
    if len(conversation_history) > 20:
        conversation_history[:] = conversation_history[-20:]

    return reply
