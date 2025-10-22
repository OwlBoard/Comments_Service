from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from src.websocket_manager import comment_connection_manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws/dashboards/{dashboard_id}/comments")
async def websocket_comments_endpoint(
    websocket: WebSocket,
    dashboard_id: str,
    user_id: str = Query(None)  # Optional query parameter
):
    """
    WebSocket endpoint for real-time comment updates on a specific dashboard.
    
    Clients connect to this endpoint to receive notifications when:
    - A new comment is created
    - A comment is updated
    - A comment is deleted
    """
    logger.info(f"WebSocket connection attempt for dashboard: {dashboard_id}, user: {user_id}")
    
    await comment_connection_manager.connect(websocket, dashboard_id)
    
    try:
        while True:
            # Keep the connection alive and listen for any messages from client
            # We don't expect clients to send data, but we need to keep the loop running
            data = await websocket.receive_text()
            logger.info(f"Received message from client on dashboard {dashboard_id}: {data}")
            
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from comments for dashboard {dashboard_id}")
        await comment_connection_manager.disconnect(websocket, dashboard_id)
    except Exception as e:
        logger.error(f"Error in WebSocket connection for dashboard {dashboard_id}: {e}")
        await comment_connection_manager.disconnect(websocket, dashboard_id)
