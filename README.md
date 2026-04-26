# 🛡️ CypherTrap AI - Intelligent Deception System

**CypherTrap AI** is a state-of-the-art, deception-based cybersecurity defense system designed to neutralize attackers using a "Hall of Mirrors" approach. Instead of traditional blocking, it traps attackers in a high-fidelity synthetic environment, feeds them deceptive data, and uses Machine Learning to analyze their behavior in real-time.

---

## 👨‍💻 Created by: **SAHIL CHAVAN**

---

## 🌟 Key Features
- **Intelligent Deception Engine**: Uses Gemini & Mistral AI to generate context-aware fake SQL results.
- **Query-Aware Simulator**: Automatically detects and responds to SQL patterns (Role filtering, Column selection).
- **ML Threat Analysis**: Built-in Isolation Forest model (Scikit-Learn) for real-time anomaly detection and threat scoring.
- **Premium Dashboard**: High-fidelity React dashboard for live attack monitoring and session tracking.
- **Credential Traps**: Generates realistic fake bcrypt hashes and cloud API keys to waste attacker resources.
- **Demo Mode**: Includes a "Vulnerable vs. Secured" comparison feature for educational presentations.

---

## 🏗️ Technology Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React + Tailwind CSS
- **AI/LLM**: Google Gemini, Mistral AI
- **ML**: Scikit-Learn (Anomaly Detection)
- **Database**: PostgreSQL (SQLAlchemy ORM)

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- PostgreSQL
- Node.js (for frontend)

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/cyphertrap
VULNERABLE_DB_URL=postgresql://user:pass@localhost:5432/hostel_finder
GEMINI_API_KEY=your_key
MISTRAL_API_KEY=your_key
```

### 3. Running the Backend
```bash
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m backend.database.init_db
python -m uvicorn backend.main:app --reload
```

### 4. Running the Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🎭 Demonstration
Use the **`attacker_bot.py`** to simulate real-time attack traffic and watch the dashboard light up!

```bash
python attacker_bot.py
```

---

## 📜 License
MIT License - Created for educational and cybersecurity research purposes.
