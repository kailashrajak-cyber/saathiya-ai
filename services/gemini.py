"""
services/gemini.py
Gemini AI Provider
"""

import google.generativeai as genai
from config import Config, SYSTEM_PROMPT

# Gemini configure
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)


def is_configured():
    return bool(Config.GEMINI_API_KEY)


def generate_reply(
    user_message: str,
    history: list,
    system_prompt: str = None,
) -> str:
    """
    Generate AI reply using Gemini.
    """

    if not Config.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY set nahi hai server par")

    system = system_prompt or SYSTEM_PROMPT

    conversation = system + "\n\n"

    for msg in history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        conversation += f"{role}: {content}\n"

    conversation += f"user: {user_message}\nassistant:"

    model = genai.GenerativeModel(Config.AI_MODEL)

    response = model.generate_content(conversation)

    if hasattr(response, "text") and response.text:
        return response.text.strip()

    return "Sorry, mujhe samajh nahi aaya. Phir se try karo?"
