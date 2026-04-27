import time
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import deception, stats, vulnerable, realtime, decoy
from backend.services.logger import AttackLogger

app = FastAPI(title="CypherTrap AI - Intelligent Deception System")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Attack Logger (singleton or service)
attack_logger = AttackLogger()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Captures malformed requests that fail Pydantic validation.
    In a deception system, we often want to log these and return a deceptive response.
    """
    client_host = request.client.host
    print(f"[THREAT_LOG] Validation Error from {client_host}: {exc}")
    
    # Return a deceptive response instead of a standard 422
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid request format",
            "details": "The server could not understand the request body.",
            "error_type": "SchemaMismatch"
        }
    )

@app.middleware("http")
async def track_attacker_request(request: Request, call_next):
    start_time = time.time()
    
    # Generate a session or request ID
    request_id = str(uuid.uuid4())
    request.state.id = request_id
    
    # Capture initial request data
    client_host = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")
    path = request.url.path
    method = request.method
    
    # Process the request
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    # Log the interaction (Asynchronously in production)
    # For Phase 1, we'll just print it or use a simple service
    await attack_logger.log_request(
        request_id=request_id,
        ip=client_host,
        user_agent=user_agent,
        path=path,
        method=method,
        status_code=response.status_code,
        duration=duration
    )
    
    return response

# Include routes
app.include_router(vulnerable.router, tags=["Legacy Vulnerable App"])
app.include_router(deception.router, tags=["Deception Layer"])
app.include_router(stats.router, prefix="/api", tags=["Statistics"])
app.include_router(realtime.router, tags=["Realtime"])
app.include_router(decoy.router, prefix="/api/decoy", tags=["Honeytrap"])

@app.get("/")
async def root():
    return {"status": "CypherTrap AI System Online", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
