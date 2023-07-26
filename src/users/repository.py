from typing import Type
from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.users.model import User
from src.utils import get_password_hash


class UserRepository:
    @staticmethod
    def save(db: Session, user: User) -> User:
        if user.user_id:
            user = db.merge(user)
        else:
            user.password = get_password_hash(user.password)
            db.add(user)
        db.commit()
        return user

    @staticmethod
    def find_all(db: Session) -> list[Type[User]]:
        return db.query(User).all()

    @staticmethod
    def find_by_id(db: Session, user_id: int) -> Type[User] | None:
        return db.query(User).filter_by(user_id=user_id).first()

    @staticmethod
    def find_by_username(db: Session, username: str) -> Type[User] | None:
        return db.query(User).filter_by(username=username).first()

    @staticmethod
    def delete_by_id(db: Session, user_id: int) -> User.user_id:
        user = db.query(User).filter_by(user_id=user_id).first()
        if user is not None:
            db.delete(user)
            db.commit()
        return user_id

    @staticmethod
    async def user_exists(db: Session, user_id: int = None, username: str = None) -> bool:
        return db.query(User).filter(or_(User.user_id == user_id, User.username == username)).first() is not None
