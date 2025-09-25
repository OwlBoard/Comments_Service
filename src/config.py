import os

class Config:
    def __init__(self):
        """
        Lee las variables de entorno en el momento de la instanciación.
        """
        self.DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://user:password@mongo_db:27017/user_db")
        self.SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8000)) 
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "un_secreto")