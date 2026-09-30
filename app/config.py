import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MYSQL_SSL_CA: str = os.getenv("MYSQL_SSL_CA")
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGODB_DB: str = os.getenv("MONGODB_DB","cart_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPTRE_MINUTES: int = 60
    
settings = Settings()