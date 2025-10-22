# src/websocket_manager.py
import json
import logging
from typing import Dict
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class CommentConnectionManager:
    def __init__(self):
        # Dashboard ID -> List of WebSockets
        self.active_connections: Dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, dashboard_id: str):
        """Connect a client to receive comment updates for a specific dashboard"""
        await websocket.accept()
        
        # Initialize dashboard connections if not exists
        if dashboard_id not in self.active_connections:
            self.active_connections[dashboard_id] = []
        
        # Add connection
        self.active_connections[dashboard_id].append(websocket)
        
        logger.info(f"[CONNECT] ✅ Client connected to dashboard '{dashboard_id}'. Total connections for this dashboard: {len(self.active_connections[dashboard_id])}, All dashboards: {list(self.active_connections.keys())}")

    async def disconnect(self, websocket: WebSocket, dashboard_id: str):
        """Disconnect a client from comment updates"""
        if dashboard_id in self.active_connections:
            if websocket in self.active_connections[dashboard_id]:
                self.active_connections[dashboard_id].remove(websocket)
                logger.info(f"Client disconnected from comments for dashboard {dashboard_id}. Remaining connections: {len(self.active_connections[dashboard_id])}")
            
            # Remove empty dashboard
            if not self.active_connections[dashboard_id]:
                del self.active_connections[dashboard_id]
                logger.info(f"No more connections for dashboard {dashboard_id}, removed from active connections")

    async def broadcast_to_dashboard(self, dashboard_id: str, message: str):
        """Broadcast a message to all clients connected to a specific dashboard"""
        logger.info(f"[BROADCAST] Dashboard: {dashboard_id}, Active dashboards: {list(self.active_connections.keys())}")
        
        if dashboard_id not in self.active_connections:
            logger.warning(f"[BROADCAST] No active connections for dashboard {dashboard_id}")
            return
        
        connections = self.active_connections[dashboard_id].copy()
        disconnected_websockets = []
        
        logger.info(f"[BROADCAST] Sending to {len(connections)} clients on dashboard {dashboard_id}: {message[:100]}...")
        
        for websocket in connections:
            try:
                await websocket.send_text(message)
                logger.info(f"[BROADCAST] ✅ Message sent successfully")
            except Exception as e:
                logger.error(f"[BROADCAST] ❌ Error sending message: {e}")
                disconnected_websockets.append(websocket)
        
        # Clean up disconnected clients
        for websocket in disconnected_websockets:
            await self.disconnect(websocket, dashboard_id)

    async def broadcast_comment_created(self, dashboard_id: str, comment_data: dict):
        """Broadcast a newly created comment to all clients on the dashboard"""
        try:
            logger.info(f"[CREATE_BROADCAST] Starting broadcast for dashboard '{dashboard_id}'")
            
            message_data = {
                "type": "comment_created",
                "data": comment_data
            }
            
            json_message = json.dumps(message_data)
            await self.broadcast_to_dashboard(dashboard_id, json_message)
            
            logger.info(f"[CREATE_BROADCAST] ✅ Completed broadcast for dashboard {dashboard_id}")
            
        except Exception as e:
            logger.error(f"[CREATE_BROADCAST] ❌ Error: {e}", exc_info=True)

    async def broadcast_comment_updated(self, dashboard_id: str, comment_data: dict):
        """Broadcast an updated comment to all clients on the dashboard"""
        try:
            message_data = {
                "type": "comment_updated",
                "data": comment_data
            }
            
            json_message = json.dumps(message_data)
            await self.broadcast_to_dashboard(dashboard_id, json_message)
            
            logger.info(f"Broadcasted comment_updated for dashboard {dashboard_id}")
            
        except Exception as e:
            logger.error(f"Error in broadcast_comment_updated: {e}")

    async def broadcast_comment_deleted(self, dashboard_id: str, comment_id: str):
        """Broadcast a deleted comment to all clients on the dashboard"""
        try:
            message_data = {
                "type": "comment_deleted",
                "data": {
                    "comment_id": comment_id
                }
            }
            
            json_message = json.dumps(message_data)
            await self.broadcast_to_dashboard(dashboard_id, json_message)
            
            logger.info(f"Broadcasted comment_deleted for dashboard {dashboard_id}")
            
        except Exception as e:
            logger.error(f"Error in broadcast_comment_deleted: {e}")

    def get_connection_count(self, dashboard_id: str) -> int:
        """Get number of clients connected to a dashboard"""
        if dashboard_id not in self.active_connections:
            return 0
        
        return len(self.active_connections[dashboard_id])

# Global instance
comment_connection_manager = CommentConnectionManager()
