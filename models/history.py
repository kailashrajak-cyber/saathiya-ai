"""
models/history.py  —  NEW FILE
Chat history ke liye do tables:
  Conversation — ek poori baatcheet (title, pin, timestamps)
  Message      — us baatcheet ke andar ek message
"""

from datetime import datetime
from models.user import db


class Conversation(db.Model):
    __tablename__ = "conversations"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title      = db.Column(db.String(200), default="Nayi Baatcheet")
    is_pinned  = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = db.relationship(
        "Message", backref="conversation", lazy="dynamic",
        cascade="all, delete-orphan", order_by="Message.id"
    )

    def to_dict(self) -> dict:
        return {
            "id":         self.id,
            "title":      self.title,
            "is_pinned":  self.is_pinned,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<Conversation {self.id}: {self.title[:30]}>"


class Message(db.Model):
    __tablename__ = "messages"

    id              = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"),
                                nullable=False, index=True)
    role            = db.Column(db.String(20), nullable=False)  # "user" | "assistant"
    content         = db.Column(db.Text, nullable=False)
    is_crisis       = db.Column(db.Boolean, default=False)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id":         self.id,
            "role":       self.role,
            "content":    self.content,
            "is_crisis":  self.is_crisis,
            "created_at": self.created_at.isoformat(),
        }
