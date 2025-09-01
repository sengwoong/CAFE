from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Ensure .env values override system envs (fixes cases where a global DATABASE_URL exists)
load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/cafe_db")

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session():
    """Return a new Session that MUST be closed by the caller.

    Prefer using `with SessionLocal() as db:` in services to ensure timely close.
    This helper exists for rare cases where a plain function call is desired.
    """
    return SessionLocal()
