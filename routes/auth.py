"""
routes/auth.py  —  NEW FILE
Auth HTTP endpoints (all under /api/auth/*).
Business logic routes/auth → services/auth.py mein hai.
"""

from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user

from models.user import db
from services.auth import (
    AuthError,
    signup_user,
    login_user_with_password,
    verify_google_token,
    generate_reset_token,
    reset_password_with_token,
)

auth_bp = Blueprint("auth", __name__)


# ─── Signup ──────────────────────────────────────────────────

@auth_bp.route("/api/auth/signup", methods=["POST"])
def signup():
    """Email + password se naya account banao."""
    data = request.get_json(silent=True) or {}
    try:
        user = signup_user(data.get("name"), data.get("email"), data.get("password"))
        login_user(user, remember=True)
        session.pop("is_guest", None)
        return jsonify({"success": True, "user": user.to_dict()}), 201
    except AuthError as e:
        return jsonify({"error": str(e)}), 400


# ─── Login ───────────────────────────────────────────────────

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """Email + password se login karo."""
    data = request.get_json(silent=True) or {}
    try:
        user = login_user_with_password(data.get("email"), data.get("password"))
        login_user(user, remember=True)
        session.pop("is_guest", None)
        return jsonify({"success": True, "user": user.to_dict()})
    except AuthError as e:
        return jsonify({"error": str(e)}), 401


# ─── Google Sign-In ──────────────────────────────────────────

@auth_bp.route("/api/auth/google", methods=["POST"])
def google_auth():
    """
    Frontend se Google credential (JWT) receive karo, verify karo, login karo.
    Requires GOOGLE_CLIENT_ID env var.
    """
    data = request.get_json(silent=True) or {}
    credential = (data.get("credential") or "").strip()
    if not credential:
        return jsonify({"error": "Google credential nahi mila"}), 400
    try:
        user = verify_google_token(credential)
        login_user(user, remember=True)
        session.pop("is_guest", None)
        return jsonify({"success": True, "user": user.to_dict()})
    except AuthError as e:
        return jsonify({"error": str(e)}), 401


# ─── Guest Mode ──────────────────────────────────────────────

@auth_bp.route("/api/auth/guest", methods=["POST"])
def guest():
    """
    Bina account ke continue karo.
    Server-side session mein sirf ek flag store hota hai.
    Chat kaam karta hai; history save nahi hoti.
    """
    logout_user()                # agar koi logged in tha
    session["is_guest"] = True
    return jsonify({"success": True, "is_guest": True})


# ─── Logout ──────────────────────────────────────────────────

@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """Session clear karo — logged-in ya guest dono ke liye."""
    logout_user()
    session.pop("is_guest", None)
    return jsonify({"success": True})


# ─── Current User ────────────────────────────────────────────

@auth_bp.route("/api/auth/me", methods=["GET"])
def me():
    """
    Frontend ke liye: kaun login hai?
    Chat page load hone par yahan se user data leta hai.
    """
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict())
    if session.get("is_guest"):
        return jsonify({"is_guest": True, "is_authenticated": False})
    return jsonify({"is_authenticated": False}), 401


# ─── Profile Update ──────────────────────────────────────────

@auth_bp.route("/api/auth/profile", methods=["PUT"])
@login_required
def update_profile():
    """Naam aur language preference update karo."""
    data = request.get_json(silent=True) or {}
    if "name" in data:
        name = (data["name"] or "").strip()
        if name:
            current_user.name = name[:80]
    if "language" in data:
        lang = (data["language"] or "hi").strip()
        current_user.language = lang[:20]
    db.session.commit()
    return jsonify({"success": True, "user": current_user.to_dict()})


# ─── Forgot Password ─────────────────────────────────────────

@auth_bp.route("/api/auth/forgot-password", methods=["POST"])
def forgot_password():
    """
    Password reset token generate karo.
    Security: hamesha same response dete hain (email enumeration prevent karne ke liye).
    Dev mein: token server logs mein print hota hai.
    Production mein: SMTP se email bhejo.
    """
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    generate_reset_token(email)  # None return karta hai agar user nahi mila (silent)
    return jsonify({"message": "Agar email registered hai, reset link bhej di gayi hai"})


@auth_bp.route("/api/auth/reset-password", methods=["POST"])
def reset_password():
    """Token + new password se password reset karo."""
    data = request.get_json(silent=True) or {}
    try:
        reset_password_with_token(data.get("token"), data.get("password"))
        return jsonify({"success": True})
    except AuthError as e:
        return jsonify({"error": str(e)}), 400
