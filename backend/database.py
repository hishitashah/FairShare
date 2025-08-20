import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .settings import get_settings

# Load environment variables from .env file
load_dotenv()

settings = get_settings()
DATABASE_URL = settings.database_url or os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Default to a local PostgreSQL connection for macOS Homebrew
    # Format: postgresql://username@localhost:5432/database_name
    DATABASE_URL = "postgresql://hishitashah@localhost:5432/fairshare"

# The engine is the main entry point for SQLAlchemy to communicate with the DB.
# echo=True will log all SQL statements, which is useful for debugging.
engine = create_engine(DATABASE_URL, echo=(settings.env == "dev"))

# A sessionmaker provides a factory for creating new Session objects.
# A Session is like a "conversation" with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is a class that all our ORM models will inherit from.
# It helps SQLAlchemy map our Python objects to database tables.
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()