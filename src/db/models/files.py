from sqlalchemy import Column, Integer, String

from src.core.db import Base, engine


class File(Base):
    __tablename__ = 'files'

    id: int = Column(Integer, primary_key=True)
    file_path: str = Column(String)


Base.metadata.create_all(engine)
