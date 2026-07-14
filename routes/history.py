from flask import Blueprint, jsonify, abort
from flask_login import login_required, current_user

from models.history import Conversation, Message

history_bp = Blueprint("history", __name__)


@history_bp.route("/api/history", methods=["GET"])
@login_required
def get_history():

    conversations = (
        Conversation.query
        .filter_by(user_id=current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    return jsonify([
        c.to_dict()
        for c in conversations
    ])


@history_bp.route("/api/history/<int:conversation_id>", methods=["GET"])
@login_required
def get_conversation(conversation_id):

    conversation = Conversation.query.filter_by(
        id=conversation_id,
        user_id=current_user.id
    ).first()

    if not conversation:
        abort(404)

    messages = (
        Message.query
        .filter_by(conversation_id=conversation.id)
        .order_by(Message.id.asc())
        .all()
    )

    return jsonify({
        "conversation": conversation.to_dict(),
        "messages": [m.to_dict() for m in messages]
    })
