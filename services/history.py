from models.user import db
from models.history import Conversation, Message


def save_chat(user_id, user_message, ai_reply, is_crisis=False):
    """
    Save a chat message to the latest conversation.
    """

    conversation = (
        Conversation.query
        .filter_by(user_id=user_id)
        .order_by(Conversation.updated_at.desc())
        .first()
    )

    if conversation is None:
        conversation = Conversation(
            user_id=user_id,
            title=user_message[:40]
        )
        db.session.add(conversation)
        db.session.commit()

    db.session.add(
        Message(
            conversation_id=conversation.id,
            role="user",
            content=user_message
        )
    )

    db.session.add(
        Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_reply,
            is_crisis=is_crisis
        )
    )

    db.session.commit()

    return conversation
