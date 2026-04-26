from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.config import get_db
from backend.models.threat import AttackLog, SessionTrace
from typing import List

router = APIRouter()

@router.get("/attacks", response_model=List[dict])
async def get_recent_attacks(limit: int = 10, db: Session = Depends(get_db)):
    """Fetch recent attack logs for the dashboard."""
    logs = db.query(AttackLog).order_by(AttackLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": str(log.id),
            "ip": log.ip_address,
            "path": log.path,
            "method": log.method,
            "status": log.status_code,
            "score": log.threat_score,
            "level": log.threat_level,
            "time": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for log in logs
    ]

@router.get("/summary")
async def get_security_summary(db: Session = Depends(get_db)):
    """Fetch aggregated security stats."""
    total_attacks = db.query(AttackLog).count()
    active_sessions = db.query(SessionTrace).filter(SessionTrace.is_active == 1).count()
    high_threat_events = db.query(AttackLog).filter(AttackLog.threat_level == "High").count()
    
    # Calculate average threat score
    avg_score = db.query(AttackLog.threat_score).all()
    avg_score_val = sum([s[0] for s in avg_score]) / len(avg_score) if avg_score else 0
    
    return {
        "total_requests": total_attacks,
        "threat_events": high_threat_events,
        "avg_threat_score": round(avg_score_val, 1),
        "trap_hits": total_attacks # In this system, every log is a trap hit
    }
