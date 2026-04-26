import logging
from datetime import datetime
from typing import Any
from backend.database.config import SessionLocal
from backend.models.threat import AttackLog, Session as AttackerSession
from backend.services.websocket import manager

class AttackLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("CypherTrap")

    async def log_attack(self, ip: str, query: str, threat_score: float, 
                         attack_type: str, threat_level: str, 
                         session_id: str, session_id_fk: Any,
                         response_type: str, endpoint: str = "/db",
                         path: str = None, method: str = None, 
                         status_code: int = 200, duration: float = 0.0):
        """
        Persists detailed attack intelligence and broadcasts live event.
        """
        db = SessionLocal()
        try:
            # 1. Save to Database
            new_log = AttackLog(
                attacker_ip=ip,
                session_id=session_id,
                session_id_fk=session_id_fk,
                endpoint=endpoint,
                path=path,
                method=method,
                status_code=status_code,
                query=query,
                threat_score=threat_score,
                threat_level=threat_level,
                attack_type=attack_type,
                response_type=response_type,
                duration=duration,
                timestamp=datetime.utcnow()
            )
            db.add(new_log)
            db.commit()

            # 2. Broadcast via WebSocket for SOC Dashboard
            event = {
                "id": str(new_log.id),
                "ip": ip,
                "session_id": session_id,
                "attack_type": attack_type,
                "threat_score": threat_score,
                "threat_level": threat_level,
                "query": query,
                "endpoint": endpoint,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            await manager.broadcast(event)
            
            self.logger.info(f"🚨 [{threat_level}] {attack_type} detected from {ip}. Score: {threat_score}")
        except Exception as e:
            self.logger.error(f"Failed to log attack: {e}")
            db.rollback()
        finally:
            db.close()

    async def log_request(self, **kwargs):
        """Logs every interaction for behavioral analysis."""
        self.logger.info(f"🌐 Request: {kwargs.get('method')} {kwargs.get('path')} from {kwargs.get('ip')}")
