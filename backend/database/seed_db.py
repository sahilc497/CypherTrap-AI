import uuid
import hashlib
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.config import DATABASE_URL, Base
from backend.models.threat import Session, AttackLog

# Database Setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_session_id(ip, ua):
    return hashlib.md5(f"{ip}:{ua}".encode()).hexdigest()

def seed():
    db = SessionLocal()
    print("Starting Forensic Data Seeding...")

    # Clear existing data for a fresh demo
    db.query(AttackLog).delete()
    db.query(Session).delete()
    db.commit()

    # 1. Attacker Profile: The SQL Specialist (Russia)
    ip1 = "95.161.226.11"
    ua1 = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    sid1 = get_session_id(ip1, ua1)
    
    attacker1 = Session(
        session_id=sid1,
        ip_address=ip1,
        user_agent=ua1,
        city="Moscow",
        country="Russia",
        latitude=55.7558,
        longitude=37.6173,
        risk_level="High",
        current_threat_score=88.5,
        request_count=12
    )

    # 2. Attacker Profile: The Botnet Node (China)
    ip2 = "117.25.132.88"
    ua2 = "python-requests/2.28.1"
    sid2 = get_session_id(ip2, ua2)
    
    attacker2 = Session(
        session_id=sid2,
        ip_address=ip2,
        user_agent=ua2,
        city="Beijing",
        country="China",
        latitude=39.9042,
        longitude=116.4074,
        risk_level="Medium",
        current_threat_score=45.0,
        request_count=45
    )

    # 3. Attacker Profile: The Local Intruder (Mumbai) - UNMASKED
    ip3 = "103.21.159.20"
    ua3 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/104.0.1293.63"
    sid3 = get_session_id(ip3, ua3)
    
    attacker3 = Session(
        session_id=sid3,
        ip_address=ip3,
        user_agent=ua3,
        city="Mumbai",
        country="India",
        latitude=19.0760,
        longitude=72.8777,
        risk_level="Critical",
        current_threat_score=99.9,
        request_count=8,
        # Placeholder for unmasked profile
        captured_face_url="https://api.dicebear.com/7.x/avataaars/svg?seed=attacker123"
    )

    db.add_all([attacker1, attacker2, attacker3])
    db.commit()

    # Seed Attack Logs
    logs = [
        # Russian Attacker Logs
        AttackLog(
            session_id_fk=attacker1.id,
            session_id=sid1,
            attacker_ip=ip1,
            endpoint="/db",
            method="POST",
            query="SELECT * FROM users WHERE id = 1 UNION SELECT user, password FROM legacy_users--",
            threat_score=92.4,
            threat_level="High",
            attack_type="SQL Injection",
            response_type="AI_Deception_Engine",
            timestamp=datetime.utcnow() - timedelta(minutes=45)
        ),
        AttackLog(
            session_id_fk=attacker1.id,
            session_id=sid1,
            attacker_ip=ip1,
            endpoint="/db",
            method="POST",
            query="SELECT name, setting FROM pg_settings WHERE name LIKE 'ssl%'",
            threat_score=78.0,
            threat_level="High",
            attack_type="Reconnaissance",
            response_type="Simulator_Enhanced",
            timestamp=datetime.utcnow() - timedelta(minutes=42)
        ),
        
        # Chinese Botnet Logs
        AttackLog(
            session_id_fk=attacker2.id,
            session_id=sid2,
            attacker_ip=ip2,
            endpoint="/db",
            method="POST",
            query="SELECT 1",
            threat_score=12.0,
            threat_level="Low",
            attack_type="Scanning",
            response_type="Simulator_Standard",
            timestamp=datetime.utcnow() - timedelta(hours=2)
        ),
        
        # Local Intruder (Mumbai) - The one who fell for the trap
        AttackLog(
            session_id_fk=attacker3.id,
            session_id=sid3,
            attacker_ip=ip3,
            endpoint="/login",
            method="POST",
            query="LOGIN_ATTEMPT: admin / ' OR 1=1--",
            threat_score=99.0,
            threat_level="Critical",
            attack_type="Credential Harvesting",
            response_type="Simulator",
            timestamp=datetime.utcnow() - timedelta(minutes=5)
        )
    ]

    db.add_all(logs)
    db.commit()
    print("Database seeded with 3 Threat Actors and their attack history.")
    db.close()

if __name__ == "__main__":
    seed()
