import json
from typing import List, Dict, Any
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages WebSocket connections for real-time attack streaming.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        """Sends an event to all connected dashboard clients."""
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                # Remove dead connections
                self.active_connections.remove(connection)

# Global manager instance
manager = ConnectionManager()
