# 🛡️ Gamified Cybersecurity Educational App

An interactive **gamified cybersecurity training platform** built with **Flask (Python)**, **SQLAlchemy**, and a **cyberpunk-themed frontend** designed with **ChatGPT** using **Tailwind/HTML**.  

The platform integrates with **MITRE Caldera** for adversary simulations and supports **AI-driven Q/A** (Google Gemini API).  


---

## 🚀 Features
- 🎨 **Frontend UI**: cyberpunk landing page, login/register screens, game dashboard — all designed with ChatGPT.
- 👥 **User accounts**: registration & login powered by Flask + SQLAlchemy.
- 🏆 **Game dashboard** (`game.html`):
  - Real-time leaderboard
  - XP/level progress
  - Badge tracking
- ❓ **Q/A phase**:
  - Tier-based difficulty
  - Timed challenges
  - XP rewards and badge unlocks
- 🕵️ **Caldera integration**:
  - Run live adversary simulations
  - Or skip them in dev mode using a toggle.
- 🤖 **AI-generated cybersecurity questions**:
  - Powered by Google Gemini API (currently under update).
  - OpenAI integration planned.

---

## ⚙️ Requirements
- Python **3.11+** → for Caldera
- Python **3.13+** → for the Flask backend  
- Docker → recommended for local testing  
- Node.js/NPM → only needed if building React/Tailwind frontend separately

---

## 🐳 Run with Docker (recommended)

1. Clone the repo:
   ```bash
   git clone https://github.com/krishpuw/Gamified-Cybersecurity-Educational-App.git
   cd Gamified-Cybersecurity-Educational-App
Build the image:

bash
Copy code
docker build -t cyber-app -f Dockerfile .
Run the container:

bash
Copy code
docker run --rm -p 5000:5000 cyber-app
Access the app at:
👉 http://localhost:5000

🖥️ Run Manually (without Docker)
1. Backend
bash
Copy code
cd Backend
python3 -m venv env
source env/bin/activate   # (Windows: env\Scripts\activate)

pip install -r requirements.txt

# Initialize DB (SQLite by default)
export FLASK_APP=app:create_app
flask db upgrade

# Start backend
python app.py
App runs at 👉 http://127.0.0.1:5000

# 🔑 Environment Variables

All secrets/configs are stored in Backend/.env.
For testing, copy the provided example file:

cd Backend
cp .env.example .env


# Database

Current: SQLite (Backend/test.db)

Planned: PostgreSQL (deployment phase)

Reset local DB:

rm -f Backend/test.db
flask db upgrade

# 🤖 Caldera Integration

Runs in a Python 3.11 environment:

cd caldera
python3.11 -m venv env311
source env311/bin/activate

python server.py --insecure --build

# CURRENT STATUS 
AI Question Generation

🛠️ Fix in progress — Q/A generation may not work until API update is complete

