from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.services.websocket import manager

router = APIRouter()

@router.websocket("/ws/attacks")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time attack streaming to the SOC dashboard.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
