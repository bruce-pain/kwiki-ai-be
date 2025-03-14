"""The database module"""

from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy import create_engine

from app.core.config import settings
from app.utils.logger import logger

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

Base = declarative_base()


def init_db():
    """Initialize the database by creating all tables defined by Base metadata."""
    return Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a new database session and ensure it's closed after use."""
    db = db_session()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database Error: {e}")
        raise
    finally:
        db.close()
