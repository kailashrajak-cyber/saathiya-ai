"""
app.py  —  MODIFIED
Entry point. DB aur Flask-Login init kiye. auth_bp register kiya.
Chat aur pages blueprints unchanged.
"""

from flask import Flask, request as flask_request, jsonify, redirect
from flask_cors import CORS
from flask_login import LoginManager

from config import Config
from models.user import db, User
from routes.chat import chat_bp
from routes.pages import pages_bp
from routes.auth import auth_bp 
from routes.history import history_bp # NEW


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)       # SECRET_KEY, SQLALCHEMY_* config load
    CORS(app)

    # ── Database ──────────────────────────────────────────────
    db.init_app(app)

    # ── Flask-Login ───────────────────────────────────────────
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        """
        API routes → 401 JSON.
        Page routes → redirect to /auth.
        """
        if flask_request.path.startswith("/api/"):
            return jsonify({"error": "Login zaroori hai", "redirect": "/auth"}), 401
        return redirect("/auth")

    # ── Blueprints ────────────────────────────────────────────
    app.register_blueprint(pages_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)      # NEW
    app.register_blueprint(history_bp)
    # ── Create DB tables ──────────────────────────────────────
    with app.app_context():
        # Import all ORM models so SQLAlchemy discovers them before create_all.
        # History / Memory tables are created now even though they're used later.
        from models import history, memory  # noqa: F401
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
