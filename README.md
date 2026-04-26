# 🛡️ CypherTrap AI - Advanced SOC & Deception Engine

**CypherTrap AI** is a state-of-the-art, deception-based cybersecurity platform designed to neutralize attackers using a "Hall of Mirrors" approach. Instead of simple blocking, it traps attackers in a high-fidelity synthetic environment, unmasks their identity using biometric honeytraps, and analyzes their behavioral risk in real-time.

---

## 👨‍💻 Created by: **SAHIL CHAVAN**

---

## 🌟 Premium Features

### 📡 Real-Time SOC Intelligence
- **Live Threat Stream**: WebSocket-powered dashboard for instant attack visualization (Zero-latency).
- **Behavioral Session Tracking**: Groups attackers by IP + User-Agent fingerprinting to track their "Attacker Journey."
- **Rolling Risk Scoring**: ML-driven threat levels (Low, Medium, High) that evolve as the attacker persists.

### 🎭 Intelligent Deception Layer
- **AI-Enriched Simulation**: Uses Gemini & Mistral AI to generate context-aware fake SQL results that trick even expert attackers.
- **Credential Harvesting Traps**: Feeds attackers realistic fake bcrypt hashes and API keys to waste their resources.

### 🕵️ Attacker Unmasking (Forensics)
- **IP Geolocation**: Automatically maps attacker IPs to physical cities and countries on the dashboard.
- **Honey-Camera Trap**: A high-security biometric decoy page that captures the **Attacker's Face** and **Precise GPS** coordinates.
- **Biometric Attribution**: View captured forensic photos of attackers directly in the SOC dashboard.

---

## 🏗️ Technology Stack
- **Backend**: FastAPI (Python) + SQLAlchemy
- **Frontend**: React + Tailwind CSS + Framer Motion + Recharts
- **ML/AI**: Scikit-Learn (Isolation Forest), Google Gemini, Mistral AI
- **Real-Time**: WebSockets (Python-FastAPI)
- **Database**: PostgreSQL with UUID-based Forensics Schema

---

## 🚀 Installation & Demo Setup

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize Forensic Database
python -m backend.database.init_db

# Run for LAN Access (Crucial for Demo)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev -- --host
```

---

## 🎮 The "Showstopper" Demo Flow

### Phase 1: The Breach (Computer B)
Target the deception endpoint using Postman or Browser:
`POST http://[YOUR_IP]:8000/db` with `{"query": "SELECT * FROM users"}`

### Phase 2: The Unmasking (The Reveal)
Navigate to the Honey-Camera Trap on Computer B:
`http://[YOUR_IP]:8000/api/decoy/admin-verify`
1. Click **Verify Identity**.
2. Grant Camera/Location access.
3. **Check the Dashboard on Computer A**: Watch as the attacker's **Real Face** and **Location** appear on the screen!

