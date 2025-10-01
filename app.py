import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_db
from src.routes.comments_routes import router as comments_router
from src.graphql.schema import graphql_app 
from src.config import Config

# Configurar CORS antes de crear la aplicación
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Se ejecuta cuando la aplicación inicia."""
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Aplicar CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API REST
app.include_router(comments_router, prefix="/comments", tags=["Comments"])
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