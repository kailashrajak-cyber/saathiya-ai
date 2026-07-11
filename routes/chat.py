from flask import Blueprint, request, jsonify

from config import CRISIS_MESSAGE
from models.chat import ChatRequest, ChatReply
from services import gemini as ai_service
from utils.crisis import is_crisis
from flask_login import current_user
from services.memory import get_memory, save_memory
from services.rate_limit import can_chat

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    """Handle a single chat turn"""

    raw_data = request.get_json(force=True, silent=True) or {}
    chat_request = ChatRequest.from_json(raw_data)

    if not chat_request.message:
        return jsonify({"error": "Message khaali nahi ho sakta"}), 400

    # -------- Free Usage Limit --------
    if current_user.is_authenticated:
        user_key = f"user_{current_user.id}"
    else:
        user_key = request.remote_addr or "guest"

    if not can_chat(user_key):
        return jsonify({
            "reply": "⚠️ Aaj ki free limit khatam ho gayi hai. Kal phir try kariye.",
            "crisis": False
        }), 429

    # -------- Crisis Check --------
    if is_crisis(chat_request.message):
        return jsonify(
            ChatReply(
                reply=CRISIS_MESSAGE,
                crisis=True
            ).to_dict()
        )

    # -------- API Check --------
    if not ai_service.is_configured():
        return jsonify({
            "error": "GEMINI_API_KEY set nahi hai server par"
        }), 500

    try:

        memory = {}

        if current_user.is_authenticated:
            memory = get_memory(current_user.id)

            text = chat_request.message.lower()

            if "mera naam" in text:
                name = (
                    chat_request.message
                    .replace("Mera naam", "")
                    .replace("mera naam", "")
                    .replace("hai", "")
                    .strip()
                )

                if name:
                    save_memory(current_user.id, "name", name)
                    memory["name"] = name

        reply_text = ai_service.generate_reply(
            chat_request.message,
            chat_request.history,
            memory=memory
        )

        return jsonify(
            ChatReply(
                reply=reply_text,
                crisis=False
            ).to_dict()
        )

    except Exception as e:
        return jsonify(
            ChatReply(
                reply="Kuch technical problem ho gaya. Thodi der me phir try karo.",
                crisis=False,
                error=str(e)
            ).to_dict()
        ), 500
