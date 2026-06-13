import os

from openai import OpenAI

client = None

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


def think(user_input: str) -> str:
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Set it in your environment or .env file.")
        client = OpenAI(api_key=api_key)

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *conversation_history],
        max_tokens=150,
    )

    reply = response.choices[0].message.content.strip()

    conversation_history.append({"role": "assistant", "content": reply})

    # Keep only the last 10 turns (20 messages: user+assistant pairs).
    if len(conversation_history) > 20:
        conversation_history[:] = conversation_history[-20:]

    return reply
