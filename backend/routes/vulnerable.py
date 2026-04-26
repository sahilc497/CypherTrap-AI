import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Connect to the REAL, vulnerable legacy database
VULNERABLE_DB_URL = os.getenv("VULNERABLE_DB_URL")
engine = create_engine(VULNERABLE_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/legacy/db")
async def vulnerable_db_access(request: QueryRequest):
    """
    WARNING: THIS IS A VULNERABLE ENDPOINT FOR DEMO PURPOSES.
    It executes raw SQL and returns real data/errors.
    """
    db = SessionLocal()
    try:
        # ❌ CRITICAL VULNERABILITY: Raw SQL execution without parameterization
        result = db.execute(text(request.query))
        
        # If it's a SELECT, return the rows
        if result.returns_rows:
            rows = [dict(row._mapping) for row in result]
            return {"status": "success", "data": rows, "source": "REAL_LEGACY_DATABASE"}
        
        db.commit()
        return {"status": "success", "message": "Query executed", "source": "REAL_LEGACY_DATABASE"}
        
    except Exception as e:
        # ❌ SECURITY RISK: Exposing raw database errors to the attacker
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
