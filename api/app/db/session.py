from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Enables connection health checks
    pool_size=5,         # Set a reasonable pool size
    max_overflow=10,     # Allow up to 10 connections beyond pool_size
    pool_timeout=30,     # Connection timeout in seconds
    pool_recycle=1800    # Recycle connections every 30 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()