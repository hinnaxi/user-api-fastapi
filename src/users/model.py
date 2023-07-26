from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from src.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String(255), nullable=False, unique=True, index=True)
    first_name: str = Column(String(255), nullable=False, index=True)
    last_name: str = Column(String(255), nullable=False, index=True)
    email: str = Column(String(255), nullable=False, unique=True, index=True)
    password: str = Column(String(255), nullable=False)
    is_active: bool = Column(Boolean, server_default="true")
    created_at: datetime = Column(DateTime(), server_default=func.now())
    updated_at: datetime = Column(DateTime(), onupdate=func.now())
