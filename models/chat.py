"""
models/chat.py
---------------
Lightweight data structures for chat requests/replies.

The project doesn't use a database yet, so these are simple plain-Python
helpers rather than ORM models. They exist so:
1. The shape of a "chat message" / "chat reply" is defined in one place.
2. When Chat History / a real database is added later, these can be
   upgraded into SQLAlchemy (or similar) models with minimal changes
   to routes/services that already use them.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ChatRequest:
    """Represents an incoming chat request from the frontend."""
    message: str
    history: List[Dict[str, str]] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict) -> "ChatRequest":
        data = data or {}
        return cls(
            message=(data.get("message") or "").strip(),
            history=data.get("history") or [],
        )


@dataclass
class ChatReply:
    """Represents an outgoing chat reply to the frontend."""
    reply: str
    crisis: bool = False
    error: str = None

    def to_dict(self) -> dict:
        payload = {"reply": self.reply, "crisis": self.crisis}
        if self.error:
            payload["error"] = self.error
        return payload
