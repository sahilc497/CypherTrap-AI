import uuid
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.database.config import Base
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String, unique=True, index=True) # Logic identifier (IP+UA hash)
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Geolocation Intel
    city = Column(String, default="Unknown")
    country = Column(String, default="Unknown")
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Forensic Intel
    captured_face_url = Column(String) # URL or Base64 of the attacker's face
    
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    request_count = Column(Integer, default=1)
    risk_level = Column(String, default="Low")
    current_threat_score = Column(Float, default=0.0)
    
    attacks = relationship("AttackLog", back_populates="session")

class AttackLog(Base):
    __tablename__ = "attack_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id_fk = Column(UUID(as_uuid=True), ForeignKey("sessions.id"))
    session_id = Column(String, index=True) # Keeping original string id for easy access
    attacker_ip = Column(String)
    endpoint = Column(String)
    path = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    query = Column(Text)
    threat_score = Column(Float)
    threat_level = Column(String)
    attack_type = Column(String)
    response_type = Column(String)
    duration = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="attacks")
