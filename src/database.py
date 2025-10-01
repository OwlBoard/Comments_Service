import motor.motor_asyncio
from beanie import init_beanie
from .config import Config
from .models import Comment

settings = Config()

async def init_db():
    """
    Inicializa la conexión a la base de datos MongoDB y Beanie.
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.DATABASE_URL
    )

    await init_beanie(database=client.get_default_database(), document_models=[Comment])