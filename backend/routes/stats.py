from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.config import get_db
from typing import List

router = APIRouter()

from backend.models.threat import AttackLog, Session as AttackerSession

@router.get("/attacks", response_model=List[dict])
async def get_recent_attacks(limit: int = 20, db: Session = Depends(get_db)):
    """Fetch recent attack logs for the live feed."""
    logs = db.query(AttackLog).order_by(AttackLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": str(log.id),
            "ip": log.attacker_ip,
            "session_id": log.session_id,
            "endpoint": log.endpoint,
            "path": log.path,
            "method": log.method,
            "status": log.status_code,
            "query": log.query,
            "threat_score": log.threat_score,
            "threat_level": log.threat_level,
            "attack_type": log.attack_type,
            "response_type": log.response_type,
            "timestamp": log.timestamp.isoformat() + "Z"
        } for log in logs
    ]

@router.get("/sessions", response_model=List[dict])
async def get_all_sessions(db: Session = Depends(get_db)):
    """List all identified attacker sessions."""
    sessions = db.query(AttackerSession).order_by(AttackerSession.last_seen.desc()).all()
    return [
        {
            "id": str(s.id),
            "session_id": s.session_id,
            "ip": s.ip_address,
            "requests": s.request_count,
            "risk_level": s.risk_level,
            "score": round(s.current_threat_score, 1),
            "last_seen": s.last_seen.isoformat() + "Z",
            "ua": s.user_agent
        } for s in sessions
    ]

@router.get("/summary")
async def get_security_summary(db: Session = Depends(get_db)):
    """Fetch high-level SOC metrics."""
    total_attacks = db.query(AttackLog).count()
    active_sessions = db.query(AttackerSession).count()
    high_risk_sessions = db.query(AttackerSession).filter(AttackerSession.risk_level == "High").count()
    
    # Calculate system-wide average threat score
    avg_score = db.query(AttackLog.threat_score).all()
    avg_score_val = sum([s[0] for s in avg_score]) / len(avg_score) if avg_score else 0
    
    return {
        "total_requests": total_attacks,
        "threat_events": total_attacks, # Every interception is a threat event in this system
        "active_sessions": active_sessions,
        "high_risk_sessions": high_risk_sessions,
        "avg_threat_score": round(avg_score_val, 1),
        "trap_hits": total_attacks
    }
