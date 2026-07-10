"""
routes/chat.py
---------------
All chat-related HTTP endpoints, as a Flask Blueprint.

Why a Blueprint:
- Keeps app.py free of endpoint logic.
- New feature areas (Login, Chat History, Voice AI, Image AI, PDF AI,
  NVIDIA AI) can each get their own routes/<feature>.py blueprint and be
  registered in app.py the same way this one is.
"""

from flask import Blueprint, request, jsonify

from config import CRISIS_MESSAGE
from models.chat import ChatRequest, ChatReply
from services import gemini as ai_service
from utils.crisis import is_crisis
from flask_login import current_user
from services.memory import get_memory, save_memory

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    """Handle a single chat turn: crisis-check, then AI reply."""
    raw_data = request.get_json(force=True, silent=True) or {}
    chat_request = ChatRequest.from_json(raw_data)

    if not chat_request.message:
        return jsonify({"error": "Message khaali nahi ho sakta"}), 400

    # Safety check happens before any AI call.
    if is_crisis(chat_request.message):
        return jsonify(ChatReply(reply=CRISIS_MESSAGE, crisis=True).to_dict())

    if not ai_service.is_configured():
        return jsonify({"error": "GEMINI_API_KEY set nahi hai server par"}), 500

    try:
      memory = {}

if current_user.is_authenticated:
    memory = get_memory(current_user.id)

    text = chat_request.message.lower()

    if "mera naam" in text:
        name = chat_request.message.replace("Mera naam", "").replace("mera naam", "").replace("hai", "").strip()

        if name:
            save_memory(current_user.id, "name", name)
            memory["name"] = name
        reply_text = ai_service.generate_reply(
            chat_request.message,
chat_request.history,
memory=memory
        )
        return jsonify(ChatReply(reply=reply_text, crisis=False).to_dict())
    except Exception as e:
        fallback = ChatReply(
            reply="Kuch technical problem ho gaya. Thodi der me phir try karo.",
            crisis=False,
            error=str(e),
        )
        return jsonify(fallback.to_dict()), 500
