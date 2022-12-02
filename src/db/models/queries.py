from sqlalchemy import Column, Integer, String

from src.core.db import Base, engine


class Query(Base):
    __tablename__ = 'queries'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, unique=True)
    full_name: str = Column(String)
    post: str = Column(String)
    job_place: str = Column(String)
    topic_work: str = Column(String)
    title_work: str = Column(String)
    annotation: str = Column(String)
    file: str = Column(String)


Base.metadata.create_all(engine)
