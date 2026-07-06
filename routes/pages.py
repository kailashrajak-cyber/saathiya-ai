"""
routes/pages.py  —  MODIFIED
Ab auth check karta hai:
  / → agar not logged in AND not guest → /auth par redirect
  /auth → login page; agar already logged in → / par redirect
  /privacy, /manifest.json, /sw.js → unchanged
"""

from flask import (
    Blueprint, render_template, send_from_directory,
    current_app, session, redirect,
)
from flask_login import current_user
from config import Config

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def home():
    """
    Main chat page.
    Access: logged-in users + guests only.
    Baki sab /auth par jaate hain.
    """
    if not current_user.is_authenticated and not session.get("is_guest"):
        return redirect("/auth")

    # Logged-in user ka data template mein pass karo
    user_data = current_user.to_dict() if current_user.is_authenticated else None

    return render_template(
        "index.html",
        user=user_data,                             # None for guest
        is_guest=session.get("is_guest", False),
        google_client_id=Config.GOOGLE_CLIENT_ID,   # Google button ke liye
    )


@pages_bp.route("/auth")
def auth_page():
    """
    Login / Signup / Guest page.
    Already logged in? → main chat page par redirect.
    """
    if current_user.is_authenticated:
        return redirect("/")
    return render_template(
        "auth.html",
        google_client_id=Config.GOOGLE_CLIENT_ID,
    )


@pages_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


@pages_bp.route("/manifest.json")
def manifest():
    return send_from_directory(
        current_app.static_folder, "manifest.json",
        mimetype="application/manifest+json",
    )


@pages_bp.route("/sw.js")
def service_worker():
    return send_from_directory(
        current_app.static_folder, "sw.js",
        mimetype="application/javascript",
    )
