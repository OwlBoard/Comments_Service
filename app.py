import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware # No longer needed
from src.database import init_db
from src.routes.comments_routes import router as comments_router
from src.routes.websocket_routes import router as websocket_router
from src.graphql.schema import graphql_app 
from src.config import Config



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Se ejecuta cuando la aplicación inicia."""
    print("=== Starting Comments Service ===")
    print(f"Registered routes:")
    for route in app.routes:
        print(f"  - {route.path} [{getattr(route, 'methods', 'WS' if 'websocket' in str(type(route)).lower() else 'N/A')}]")
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# CORS is now handled by the NGINX gateway
# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "http://localhost:8080",
# ]
# 
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# API REST
app.include_router(comments_router, prefix="/comments", tags=["Comments"])
# WebSocket
app.include_router(websocket_router, prefix="/comments", tags=["WebSocket"])
# API GraphQL
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    settings = Config()
    uvicorn.run(
        "app:app",
        host=os.getenv("SERVICE_HOST", "0.0.0.0"),
        port=settings.SERVICE_PORT,
        reload=True
    )