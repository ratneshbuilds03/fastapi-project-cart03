from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

connect_args = (
    {"ssl": {"ca": settings.MYSQL_SSL_CA}} if settings.MYSQL_SSL_CA else {}
)
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autoflush = False, bind = engine, autocommit = False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()