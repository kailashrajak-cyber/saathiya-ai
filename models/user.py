"""
models/user.py  —  MODIFIED
User database model.
Naya: google_id, profile_photo, language columns.
password_hash ab nullable=True hai (Google users ke paas password nahi hota).
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(80),  nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)   # Google users ke liye null
    google_id     = db.Column(db.String(128), unique=True, nullable=True)
    profile_photo = db.Column(db.String(512), nullable=True)   # URL (Google photo ya manual)
    language      = db.Column(db.String(20),  default="hi")    # AI memory ke liye
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (cascade delete — user delete hone par sab kuch delete ho jaye)
    conversations = db.relationship(
        "Conversation", backref="user", lazy="dynamic",
        cascade="all, delete-orphan"
    )
    memories = db.relationship(
        "UserMemory", backref="user", lazy="dynamic",
        cascade="all, delete-orphan"
    )

    # ---- Password helpers ----

    def set_password(self, raw: str) -> None:
        """Plain-text password kabhi save mat karo."""
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, raw)

    # ---- Serialization ----

    def to_dict(self) -> dict:
        return {
            "id":           self.id,
            "name":         self.name,
            "email":        self.email,
            "photo":        self.profile_photo or "",
            "language":     self.language or "hi",
            "joined":       self.created_at.strftime("%B %Y"),
            "is_guest":     False,
            "is_authenticated": True,
        }

    def __repr__(self):
        return f"<User {self.email}>"
