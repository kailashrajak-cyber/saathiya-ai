"""
utils/crisis.py
----------------
Helper utilities for detecting self-harm / crisis language in user messages.

Kept separate from the AI service and routes so it can be reused by future
features (e.g. Voice AI transcripts, PDF AI extracted text) without having
to touch chat-specific code.
"""

from config import CRISIS_KEYWORDS


def is_crisis(text: str) -> bool:
    """
    Return True if the given text contains any known crisis/self-harm keyword.

    This is a simple, fast, keyword-based check - not a clinical assessment.
    It exists purely to trigger an immediate, safe, supportive response and
    helpline information before any AI call is made.
    """
    lower = text.lower()
    return any(keyword in lower for keyword in CRISIS_KEYWORDS)
