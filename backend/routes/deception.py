import asyncio
import random
import time
from fastapi import APIRouter, Request, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.services.ai_engine import AIDeceptionEngine
from backend.services.simulator import DeceptionSimulator
from backend.services.analyzer import ThreatAnalyzer
from backend.services.logger import AttackLogger
from backend.services.classifier import AttackClassifier
from backend.services.session_manager import SessionManager
from backend.database.config import get_db
from sqlalchemy.orm import Session as DBSession

# Request Model
class DbQuery(BaseModel):
    query: str
    session_id: Optional[str] = "default_session"

router = APIRouter()
ai_engine = AIDeceptionEngine()
simulator = DeceptionSimulator()
analyzer = ThreatAnalyzer()
classifier = AttackClassifier()
logger = AttackLogger()

@router.post("/db")
async def fake_db_query(db_body: DbQuery, request: Request, background_tasks: BackgroundTasks, db: DBSession = Depends(get_db)):
    """
    Intelligent Deception System Endpoint with Session Tracking.
    """
    query = db_body.query
    start_time = time.time()
    
    # 1. Session Management
    session_mgr = SessionManager(db)
    attacker_session = session_mgr.get_or_create_session(request)
    
    # 2. Performance Realism
    latency = random.uniform(0.05, 0.25)
    await asyncio.sleep(latency)

    # 2. Internal Monitoring
    print(f"[THREAT_ANALYSIS] Incoming Query: {query}")

    # 3. ML Threat Analysis (Real Isolation Forest)
    threat_intel = analyzer.analyze(query)
    threat_score = threat_intel["threat_score"]
    
    # 4. Attack Classification
    attack_type = classifier.classify(query, threat_score)
    insight = classifier.get_insight(attack_type, threat_score)

    # Update session metrics
    session_mgr.update_session_threat(attacker_session, threat_score)

    # 5. Behavior Adaptation (VERY IMPORTANT)
    # Deception Depth increases with threat score
    if threat_score > 85:
        # High Threat: Force AI Engine for maximum realism and deeper traps
        response_data = await ai_engine.generate_fake_db_result(query)
        generated_by = "AI_Deception_Engine"
    elif threat_score > 40:
        # Medium Threat: Use simulator with enhanced rules
        response_data = simulator.simulate_query(query)
        generated_by = "Simulator_Enhanced"
    else:
        # Low Threat: Standard simulator response
        response_data = simulator.simulate_query(query)
        generated_by = "Simulator_Standard"

    # 6. Background Logging (Logging Upgrade)
    background_tasks.add_task(
        logger.log_attack,
        ip=request.client.host,
        query=query,
        threat_score=threat_score,
        attack_type=attack_type,
        threat_level=threat_intel["threat_level"],
        session_id=attacker_session.session_id,
        session_id_fk=attacker_session.id,
        response_type=generated_by,
        endpoint="/db",
        path=request.url.path,
        method=request.method,
        status_code=200,
        duration=time.time() - start_time
    )

    # 7. Final response assembly (User requested format)
    return {
        "status": "success",
        "data": response_data.get("data", []),
        "query_executed": query,
        "execution_time": f"{round(time.time() - start_time, 4)}s",
        "generated_by": generated_by,
        "threat_intel": {
            "score": threat_score,
            "level": threat_intel["threat_level"],
            "type": attack_type,
            "confidence": threat_intel["confidence"]
        },
        "insight": insight,
        "server_latency": f"{round(latency * 1000, 2)}ms"
    }

@router.post("/login")
async def fake_login(request: Request, background_tasks: BackgroundTasks):
    """Fake login endpoint to capture credentials and score behavior."""
    try:
        body = await request.json()
    except Exception:
        body = {}
        
    # Analyze login attempt behavior
    username = body.get('username', 'unknown')
    threat_score = 45.0 if len(username) > 20 else 15.0
    
    # Log credential theft attempt
    background_tasks.add_task(
        logger.log_attack,
        ip=request.client.host,
        query=f"LOGIN_ATTEMPT: {username}",
        threat_score=threat_score,
        attack_type="Credential Harvesting",
        threat_level="Medium" if threat_score > 30 else "Low",
        session_id="auth_session",
        response_type="Simulator"
    )

    return {
        "status": "error",
        "message": "Invalid credentials",
        "details": "The username or password provided is incorrect."
    }
