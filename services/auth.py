"""
services/auth.py  —  MODIFIED
Auth business logic: signup, login, Google OAuth, forgot-password.
Routes sirf HTTP handle karte hain; asli kaam yahan hota hai.
"""

import logging
from config import Config
from models.user import db, User

log = logging.getLogger(__name__)


class AuthError(Exception):
    """User-friendly auth failure. Message frontend par dikhaya ja sakta hai."""
    pass


# ──────────────────────────────────────────────
#  Email / Password
# ──────────────────────────────────────────────

def signup_user(name: str, email: str, password: str) -> User:
    """Naya account banao. Duplicate ya weak password hone par AuthError."""
    name     = (name     or "").strip()
    email    = (email    or "").strip().lower()
    password = (password or "")

    if not name or not email or not password:
        raise AuthError("Naam, email aur password sab zaroori hain")
    if len(password) < 6:
        raise AuthError("Password kam se kam 6 characters ka hona chahiye")
    if User.query.filter_by(email=email).first():
        raise AuthError("Is email se pehle se account bana hua hai")

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def login_user_with_password(email: str, password: str) -> User:
    """Credentials verify karo. Galat hone par AuthError."""
    email = (email or "").strip().lower()
    user  = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password or ""):
        raise AuthError("Email ya password galat hai")
    return user


# ──────────────────────────────────────────────
#  Google OAuth
# ──────────────────────────────────────────────

def verify_google_token(credential: str) -> User:
    """
    Google credential (JWT) verify karo, User return karo.
    Pehle se registered ho to wahi return hoga; naya ho to create hoga.
    Requires: GOOGLE_CLIENT_ID env var aur google-auth package.
    """
    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests as g_requests
    except ImportError:
        raise AuthError("google-auth package install nahi hai (pip install google-auth)")

    if not Config.GOOGLE_CLIENT_ID:
        raise AuthError("GOOGLE_CLIENT_ID .env mein set nahi hai")

    try:
        idinfo = id_token.verify_oauth2_token(
            credential,
            g_requests.Request(),
            Config.GOOGLE_CLIENT_ID,
        )
    except Exception as exc:
        raise AuthError(f"Google token invalid: {exc}")

    google_id = idinfo["sub"]
    email     = idinfo.get("email", "")
    name      = idinfo.get("name", "User")
    photo     = idinfo.get("picture", "")

    # Pehle google_id se dhundo, phir email se
    user = User.query.filter_by(google_id=google_id).first()
    if not user and email:
        user = User.query.filter_by(email=email).first()

    if user:
        # Purane user ko Google ID se link karo agar nahi hai
        if not user.google_id:
            user.google_id = google_id
        if not user.profile_photo and photo:
            user.profile_photo = photo
        db.session.commit()
    else:
        # Bilkul naya user
        user = User(name=name, email=email, google_id=google_id, profile_photo=photo)
        db.session.add(user)
        db.session.commit()

    return user


# ──────────────────────────────────────────────
#  Forgot Password (token-based)
# ──────────────────────────────────────────────

def generate_reset_token(email: str) -> str | None:
    """
    Password reset token banao.
    Returns token string if user exists, else None.
    Production mein: is token ko email se bhejo.
    """
    from itsdangerous import URLSafeTimedSerializer
    user = User.query.filter_by(email=email.strip().lower()).first()
    if not user:
        return None

    s     = URLSafeTimedSerializer(Config.SECRET_KEY)
    token = s.dumps(email, salt="pw-reset")
    log.info("🔑 Password reset token for %s: %s", email, token)
    return token


def reset_password_with_token(token: str, new_password: str) -> User:
    """Token verify karo aur password update karo."""
    from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

    if len(new_password or "") < 6:
        raise AuthError("Password kam se kam 6 characters ka hona chahiye")

    s = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = s.loads(token, salt="pw-reset", max_age=3600)  # 1 ghante ka token
    except SignatureExpired:
        raise AuthError("Reset link expire ho gaya. Dobara request karo.")
    except BadSignature:
        raise AuthError("Reset link invalid hai.")

    user = User.query.filter_by(email=email).first()
    if not user:
        raise AuthError("User nahi mila")

    user.set_password(new_password)
    db.session.commit()
    return user
