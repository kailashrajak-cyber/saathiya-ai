"""
config/__init__.py  —  MODIFIED
Central configuration. Sirf environment variables yahan se aate hain.
Naya: GOOGLE_CLIENT_ID, SECRET_KEY (pehle reserved tha, ab active)
"""

import os


class Config:
    # --- AI Provider (Anthropic Claude) ---
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    AI_MODEL          = os.environ.get("AI_MODEL", "claude-sonnet-4-6")
    AI_MAX_TOKENS     = int(os.environ.get("AI_MAX_TOKENS", 1000))

    # --- Server ---
    PORT  = int(os.environ.get("PORT", 5000))
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    # --- Auth ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE-THIS-IN-PRODUCTION-USE-RANDOM-STRING")
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")   # Google Cloud Console se milega

    # --- Database ---
    SQLALCHEMY_DATABASE_URI     = os.environ.get("DATABASE_URL", "sqlite:///saathiya.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Chat ---
    MAX_HISTORY_MESSAGES = 20

    # --- Future ---
    # NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY")
    # SMTP settings for password reset emails:
    # MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    # MAIL_PORT   = int(os.environ.get("MAIL_PORT", 587))
    # MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


# ---------- System Prompt ----------

SYSTEM_PROMPT = """You are Saathiya AI, a supportive companion for teenagers aged 13-18 in India.

Your job is to help teenagers in simple, friendly Hindi (Hinglish is fine) about health, body, and emotional wellbeing topics.

Rules:
- Always respond in simple, easy Hindi/Hinglish a teenager can understand. Avoid medical jargon.
- Be respectful, warm, and completely non-judgmental, no matter what is shared.
- Explain health and body-related topics (puberty, periods, skin, diet, sleep, stress, emotions, relationships) in educational, age-appropriate language.
- Never diagnose any disease or condition with certainty. You are not a doctor.
- If symptoms sound serious or concerning, gently and clearly advise the user to talk to a doctor, parent, guardian, teacher, counselor, or another trusted adult.
- Keep answers short (3-5 sentences), clear, and supportive. Avoid long lectures.
- Protect privacy: never ask for the user's name, address, school, phone number, or other unnecessary personal details.
- If the user mentions self-harm, suicide, abuse, or severe emotional distress: respond with calm compassion first, do not try to assess risk yourself, and clearly share these helplines: iCall - 9152987821, KIRAN Helpline - 1800-599-0019 (24x7). Encourage them to also talk to a trusted adult right away.
- Never shame or lecture the user for asking something personal or sensitive.
- If the question is outside health/body/emotional wellbeing topics, gently redirect and remind them what you can help with."""


# ---------- Crisis Detection ----------

CRISIS_KEYWORDS = [
    "suicide", "khud ko khatam", "marna chahta", "marna chahti", "jeena nahi chahta",
    "jeene ka mann nahi", "khud ko nuksaan", "self harm", "cutting", "khatam kar du",
    "zindagi khatam", "mar jaana chahta", "mar jaana chahti", "khud ko maar"
]

CRISIS_MESSAGE = (
    "Lagta hai tum kisi bahut mushkil pal se guzar rahe ho. Tum akele nahi ho, "
    "aur jo feel kar rahe ho usko share karna bahut bahadur kadam hai.\n\n"
    "Please abhi kisi se baat karo:\n"
    "iCall — 9152987821 (Mon-Sat, 10am-8pm)\n"
    "KIRAN Helpline — 1800-599-0019 (24x7, free)\n\n"
    "Iske saath kisi trusted adult — parent, teacher, ya counselor se bhi baat karna, jitna jaldi ho sake."
)
