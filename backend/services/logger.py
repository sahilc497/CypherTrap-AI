from backend.database.config import SessionLocal
from backend.models.threat import AttackLog, SessionTrace
from backend.services.analyzer import ThreatAnalyzer
import logging
from datetime import datetime
import json

logger = logging.getLogger("AttackLogger")
analyzer = ThreatAnalyzer()

class AttackLogger:
    def __init__(self):
        pass

    async def log_request(self, request_id, ip, user_agent, path, method, status_code, duration):
        # 0. Calculate Threat Score using ML/Rules
        threat_score, threat_level = await analyzer.calculate_threat_score(ip, path, method, duration)

        # Create a new DB session
        db = SessionLocal()
        try:
            # 1. Save Attack Log
            attack_entry = AttackLog(
                request_id=request_id,
                ip_address=ip,
                user_agent=user_agent,
                path=path,
                method=method,
                status_code=status_code,
                duration=duration,
                threat_score=threat_score,
                threat_level=threat_level
            )
            db.add(attack_entry)


            # 2. Update or Create Session
            session = db.query(SessionTrace).filter(SessionTrace.ip_address == ip).first()
            if not session:
                session = SessionTrace(
                    session_id=f"sess_{ip.replace('.', '_')}",
                    ip_address=ip,
                    total_requests=1
                )
                db.add(session)
            else:
                session.total_requests += 1
                session.last_seen = datetime.utcnow()
                if threat_score > session.max_threat_score:
                    session.max_threat_score = threat_score

            db.commit()
            logger.warning(f"PERSISTED TRAP: {method} {path} from {ip}")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to log attack to DB: {e}")
        finally:
            db.close()

