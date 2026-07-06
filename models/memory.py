"""
models/memory.py  —  NEW FILE
AI Memory: user ke preferences aur context store karne ke liye.
Key-value store — ek user ke paas multiple memory entries ho sakti hain.
Example keys: "language", "topics_of_interest", "name", "age_group"
"""

from datetime import datetime
from models.user import db


class UserMemory(db.Model):
    __tablename__ = "user_memories"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"),
                           nullable=False, index=True)
    key        = db.Column(db.String(100), nullable=False)
    value      = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Ek user ke paas ek key ek baar hi ho sakti hai
    __table_args__ = (
        db.UniqueConstraint("user_id", "key", name="uq_user_memory_key"),
    )

    def __repr__(self):
        return f"<Memory user={self.user_id} {self.key}={self.value[:20]}>"
