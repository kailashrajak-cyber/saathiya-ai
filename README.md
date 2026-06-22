<div align="center">

<img src="https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge" alt="Live">
<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python">
<img src="https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask" alt="Flask">
<img src="https://img.shields.io/badge/Gemini-AI-orange?style=for-the-badge&logo=google" alt="Gemini">
<img src="https://img.shields.io/badge/PWA-Installable-purple?style=for-the-badge" alt="PWA">

# 🪔 Saathiya AI

**A Hindi/Hinglish AI health companion for Indian teenagers (13–18)**

*Judgment-free · Privacy-first · Crisis-aware · PWA installable*

🔗 **[Live Demo →](https://saathiya-ai-1.onrender.com)**

</div>

---

## 📌 About

Saathiya AI is a full-stack AI chatbot that helps Indian teenagers ask health, body, and emotional wellbeing questions in simple Hindi or Hinglish — without fear of judgment. It uses Google Gemini to generate warm, educational responses with built-in safety for sensitive topics.

> Built entirely from an Android phone — no laptop, no local dev environment.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 AI Replies | Powered by Google Gemini 2.5 Flash — responses in simple Hindi/Hinglish |
| 🛡️ Crisis Safety Net | Detects self-harm/suicide keywords → instantly shows iCall & KIRAN helplines |
| 📋 Copy Button | One-tap copy on every AI reply |
| 🎤 Voice Input | Speak your question in Hindi (Chrome supported) |
| 🔄 New Chat | Reset conversation anytime with one tap |
| 📱 PWA | Installable on Android/iPhone — no Play Store needed |
| 🔒 Privacy-First | No login, no data stored, no personal info collected |
| ⚕️ Safe Guidance | Never diagnoses — always recommends trusted adults/doctors for serious concerns |

---

## 🏗️ Architecture

```
User (Browser / PWA)
        │
        ▼
  Flask Backend (Render.com)
  ┌─────────────────────────┐
  │  app.py                 │
  │  • /api/chat endpoint   │
  │  • Crisis keyword check │
  │  • System prompt        │
  └──────────┬──────────────┘
             │
             ▼
    Google Gemini API
    (gemini-2.5-flash)
```

---

## 🧰 Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (PWA + Service Worker)
- **Backend:** Python, Flask, Flask-CORS
- **AI:** Google Gemini API (`gemini-2.5-flash`) — free tier
- **Hosting:** Render.com (free tier, auto-deploy from GitHub)
- **Design:** Custom dark UI with marigold/teal palette, animated SVG diya icon

---

## 📁 Project Structure

```
saathiya-ai/
├── app.py                  # Flask backend + /api/chat endpoint
├── templates/
│   ├── index.html          # Main chat UI
│   └── privacy.html        # Privacy policy page
├── static/
│   ├── manifest.json       # PWA manifest
│   ├── sw.js               # Service worker (network-first caching)
│   ├── icon-192.png        # App icon
│   └── icon-512.png        # App icon (large)
├── requirements.txt        # Python dependencies
├── render.yaml             # Render.com deployment config
├── .env.example            # Environment variable template
└── .gitignore
```

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/kailashrajak-cyber/saathiya-ai.git
cd saathiya-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export GEMINI_API_KEY=your_key_here

# 4. Run the app
python app.py
# Open http://localhost:5000
```

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com) — no credit card needed.

---

## 📲 Install as App (PWA)

**Android (Chrome):** Open live link → tap "📲 App Install Karo" in header → Home screen pe icon aa jaayega

**iPhone (Safari):** Open live link → Share (⬆️) → "Add to Home Screen"

---

## ⚠️ Disclaimer

Saathiya AI is an educational tool only. It is not a substitute for professional medical or mental health advice. For serious concerns, always consult a doctor, parent, guardian, or counselor.

---

## 👨‍💻 Developer

**Kailash Rajak**
B.Tech CSE (Cyber Security) — AKS University, Satna (MP)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/kailash-rajak-39b571386)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/kailashrajak-cyber)
