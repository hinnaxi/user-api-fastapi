import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from src.config import settings
from src.constants import DB_NAMING_CONVENTION

logger = logging.getLogger(__name__)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
db_engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base(metadata=metadata)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(e)
        db.rollback()
    finally:
        db.close()
