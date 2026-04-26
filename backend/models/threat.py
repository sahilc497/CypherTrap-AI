from backend.database.config import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime

class AttackLog(Base):
    __tablename__ = "attack_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    user_agent = Column(String)
    path = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    duration = Column(Float)
    
    # ML/AI Insights
    threat_score = Column(Float, default=0.0)
    threat_level = Column(String, default="Low") # Low, Medium, High
    anomaly_score = Column(Float, default=0.0)
    
    # Summary of behavior
    behavior_summary = Column(String, nullable=True)

class SessionTrace(Base):
    """Aggregated session data for attackers."""
    __tablename__ = "sessions"
    
    session_id = Column(String, primary_key=True, index=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    total_requests = Column(Integer, default=0)
    max_threat_score = Column(Float, default=0.0)
    is_active = Column(Integer, default=1)
