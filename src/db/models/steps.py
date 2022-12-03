from sqlalchemy import Column, Integer, String, Date

from src.core.db import Base, engine


class Step(Base):
    __tablename__ = 'steps'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True)
    deadline: str = Column(Date)


Base.metadata.create_all(engine)
