import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key) if api_key else None

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


def is_crisis(text):
    lower = text.lower()
    return any(keyword in lower for keyword in CRISIS_KEYWORDS)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/manifest.json")
def manifest():
    return send_from_directory(
        app.static_folder, "manifest.json", mimetype="application/manifest+json"
    )


@app.route("/sw.js")
def service_worker():
    return send_from_directory(app.static_folder, "sw.js", mimetype="application/javascript")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    user_message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not user_message:
        return jsonify({"error": "Message khaali nahi ho sakta"}), 400

    if is_crisis(user_message):
        return jsonify({"reply": CRISIS_MESSAGE, "crisis": True})

    if client is None:
        return jsonify({"error": "ANTHROPIC_API_KEY set nahi hai server par"}), 500

    messages = list(history) + [{"role": "user", "content": user_message}]
    messages = messages[-20:]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=messages
        )
        reply_text = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()
        if not reply_text:
            reply_text = "Sorry, mujhe samajh nahi aaya. Phir se try karo?"
        return jsonify({"reply": reply_text, "crisis": False})
    except Exception as e:
        return jsonify({
            "reply": "Kuch technical problem ho gaya. Thodi der me phir try karo.",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
