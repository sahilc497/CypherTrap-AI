import hashlib
from datetime import datetime
from sqlalchemy.orm import Session as DBSession
from backend.models.threat import Session as AttackerSession
from fastapi import Request
from backend.services.geo import GeolocationService

class SessionManager:
    """
    Manages attacker sessions based on IP and User-Agent.
    Tracks behavioral patterns, risk levels, and physical location.
    """
    def __init__(self, db: DBSession):
        self.db = db
        self.geo = GeolocationService()

    def get_or_create_session(self, request: Request) -> AttackerSession:
        """
        Identifies a session based on IP and User-Agent.
        Creates a new session if one doesn't exist for the pair.
        """
        ip = request.client.host
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Create a unique session key
        session_key = hashlib.md5(f"{ip}:{user_agent}".encode()).hexdigest()
        
        session = self.db.query(AttackerSession).filter(AttackerSession.session_id == session_key).first()
        
        if not session:
            # New session - Get location intel
            location = self.geo.get_location(ip)
            
            session = AttackerSession(
                session_id=session_key,
                ip_address=ip,
                user_agent=user_agent,
                city=location["city"],
                country=location["country"],
                latitude=location["lat"],
                longitude=location["lon"],
                first_seen=datetime.utcnow(),
                last_seen=datetime.utcnow(),
                request_count=1,
                risk_level="Low",
                current_threat_score=0.0
            )
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
        else:
            session.last_seen = datetime.utcnow()
            session.request_count += 1
            self.db.commit()
            
        return session

    def update_session_threat(self, session: AttackerSession, threat_score: float):
        """
        Updates session risk metrics based on the latest threat score.
        """
        # Calculate new rolling average threat score
        old_count = session.request_count - 1
        if old_count < 0: old_count = 0
        
        session.current_threat_score = ((session.current_threat_score * old_count) + threat_score) / session.request_count
        
        # Adjust risk level
        if session.current_threat_score > 70 or session.request_count > 50:
            session.risk_level = "High"
        elif session.current_threat_score > 30 or session.request_count > 10:
            session.risk_level = "Medium"
        else:
            session.risk_level = "Low"
            
        self.db.commit()
