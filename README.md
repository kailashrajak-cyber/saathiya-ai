# Saathiya AI 🪔

Ek supportive AI companion jo teenagers (13-18 saal) ki health, body, aur emotional wellbeing se related sawaalon mein simple Hindi/Hinglish me judgment-free help karta hai.

## Features

- Simple, friendly Hindi/Hinglish responses — koi medical jargon nahi
- Kabhi bhi disease ka pakka diagnosis nahi karta — sirf educational guidance deta hai
- Serious symptoms ya distress dikhne par doctor/parent/counselor se baat karne ki salah deta hai
- Built-in crisis safety net: self-harm/suicide ke keywords detect hote hi turant iCall aur KIRAN helpline numbers dikhata hai
- Privacy-first — naam, address, phone number jaisi koi personal detail nahi maangta
- Quick topic chips (Acne, Stress, Sleep, Period cramps, Diet, Body changes)

## Tech Stack

- **Frontend:** HTML, CSS, vanilla JavaScript (`templates/index.html`)
- **Backend:** Python Flask (`app.py`) — API key ko server par safe rakhta hai
- **AI:** Anthropic Claude API (`claude-sonnet-4-6`)

## Folder Structure

```
saathiya-ai/
├── app.py              # Flask backend + /api/chat endpoint
├── templates/
│   └── index.html      # Chat UI
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── render.yaml         # Render.com deployment config
└── .gitignore
```

## App Install Karna (PWA — Play Store ki zaroorat nahi)

Saathiya AI ek PWA (Progressive Web App) hai — hosting ke baad ye seedha phone pe app jaisa install ho sakta hai, bilkul free, Play Store ke bina:

**Android (Chrome):**
1. Live link kholo
2. Header me "📲 App Install Karo" button dabao (ya Chrome menu → "Install app")
3. Home screen pe icon aa jaayega, app jaisa khulega

**iPhone (Safari):**
1. Live link kholo
2. Share button (⬆️) dabao → "Add to Home Screen" choose karo

Note: PWA install karne ke liye site HTTPS pe hosted honi chahiye — Render automatically HTTPS deta hai, isliye extra setup ki zaroorat nahi.

## Deploy Karna (sirf mobile se bhi ho sakta hai)

1. Saare files ek GitHub repo me upload kar do (jaise tumne SOC-Dashboard project ke saath kiya tha).
2. [console.anthropic.com](https://console.anthropic.com) pe account banao aur ek API key generate karo.
3. [render.com](https://render.com) pe GitHub se sign up karo.
4. Dashboard me **New → Web Service** par tap karo, apna GitHub repo connect karo.
5. Settings me:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. **Environment** tab me jaakar `ANTHROPIC_API_KEY` add karo (apni key paste karo).
7. **Deploy** dabao — kuch minute me live URL mil jaayega (jaise `https://saathiya-ai.onrender.com`).
8. Yahi live link apne GitHub README/profile me daal do recruiters ke liye.

## Important Note

Anthropic API usage paid hai (shuru me kuch free credits milte hain, uske baad usage ke hisaab se billing hoti hai). Apna API key kabhi bhi frontend code ya public repo me directly mat daalna — isi liye backend (`app.py`) banaya gaya hai jo key ko safe rakhta hai.

## Disclaimer

Saathiya AI doctor nahi hai. Ye ek educational/supportive tool hai. Serious health ya mental health concern ho to hamesha kisi doctor, parent, guardian, ya counselor se baat karo.
