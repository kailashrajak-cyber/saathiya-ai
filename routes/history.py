from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from models.history import Conversation

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
