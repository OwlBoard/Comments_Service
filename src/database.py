import motor.motor_asyncio
from beanie import init_beanie
from .config import Config
from .models import Comment # Importa tus modelos de Beanie

settings = Config()

async def init_db():
    """
    Inicializa la conexión a la base de datos MongoDB y Beanie.
    """
    # Crea el cliente de Motor para conectar a MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.DATABASE_URL
    )

    # Inicializa Beanie con la base de datos y los modelos
    # Beanie buscará la base de datos desde la URL de conexión
    await init_beanie(database=client.get_default_database(), document_models=[Comment])