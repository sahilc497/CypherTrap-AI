from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Dict, Any, List
from backend.services.ai_engine import AIDeceptionEngine
from backend.services.simulator import DeceptionSimulator

# Request Model
class DbQuery(BaseModel):
    query: str

router = APIRouter()
ai_engine = AIDeceptionEngine()
simulator = DeceptionSimulator()

@router.post("/login")
async def fake_login(request: Request):
    """Fake login endpoint to capture credentials."""
    try:
        body = await request.json()
    except Exception:
        body = {}
        
    return {
        "status": "error",
        "message": "Invalid credentials",
        "details": "The username or password provided is incorrect."
    }

@router.get("/config")
async def fake_config():
    """Fake system configuration endpoint."""
    return {
        "version": "4.2.1-stable",
        "environment": "production",
        "services": {
            "auth": "running",
            "database": "running",
            "cache": "running"
        },
        "debug_mode": False,
        "internal_ip": "10.0.0.5"
    }

@router.post("/db")
async def fake_db_query(db_body: DbQuery):
    """
    Query-Aware Fake Database Endpoint.
    Parses roles and columns to provide realistic deception.
    """
    query = db_body.query
    
    # Simulate the query results based on SQL logic
    response_data = simulator.simulate_query(query)
    
    # Enrichment: If the query is complex (e.g. UNION), use LLM for deep deception
    if "UNION" in query.upper() or "JOIN" in query.upper():
        ai_data = await ai_engine.generate_fake_db_result(query)
        if isinstance(ai_data, list):
            response_data["data"] = ai_data

    return response_data
