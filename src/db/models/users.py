from sqlalchemy import Column, Integer, String

from src.core.db import Base, engine


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, unique=True)
    hashed_password: str = Column(String)
    role: str = Column(String)


Base.metadata.create_all(engine)