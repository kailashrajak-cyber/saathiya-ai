"""
services/gemini.py  —  MODIFIED
AI provider layer. File ka naam "gemini.py" rakha gaya hai (as requested),
lekin actual provider Anthropic Claude API hai.
Naya: generate_reply ab optional custom system_prompt accept karta hai
      (memory-augmented prompt inject karne ke liye).
"""

import anthropic
from config import Config, SYSTEM_PROMPT

# Ek baar client banao — agar key nahi hai to None
_client = (
    anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    if Config.ANTHROPIC_API_KEY else None
)


def is_configured() -> bool:
    return _client is not None


def generate_reply(
    user_message: str,
    history: list,
    system_prompt: str = None,   # ← NAYA PARAMETER
) -> str:
    """
    AI se reply generate karo.

    Args:
        user_message:  user ka nayi message
        history:       purane {role, content} messages
        system_prompt: agar None, default SYSTEM_PROMPT use hoga;
                       logged-in users ke liye memory-augmented prompt aata hai

    Raises:
        RuntimeError: agar API key nahi hai
    """
    if _client is None:
        raise RuntimeError("ANTHROPIC_API_KEY set nahi hai server par")

    system = system_prompt or SYSTEM_PROMPT

    messages = list(history) + [{"role": "user", "content": user_message}]
    messages = messages[-Config.MAX_HISTORY_MESSAGES:]

    response = _client.messages.create(
        model=Config.AI_MODEL,
        max_tokens=Config.AI_MAX_TOKENS,
        system=system,
        messages=messages,
    )

    reply = "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()

    return reply or "Sorry, mujhe samajh nahi aaya. Phir se try karo?"
