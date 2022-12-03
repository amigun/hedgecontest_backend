from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint

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


class AcceptedQuery(Base):
    __tablename__ = 'accepted_query'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, unique=True)
    full_name: str = Column(String)
    post: str = Column(String)
    job_place: str = Column(String)
    topic_work: str = Column(String)
    title_work: str = Column(String)
    annotation: str = Column(String)
    file: str = Column(String)


class Score(Base):
    __tablename__ = 'scores'
    __table_args__ = (
        PrimaryKeyConstraint('id_query', 'id_expert'),
    )

    id_query: int = Column(Integer, ForeignKey('queries.id'))
    id_expert: int = Column(Integer, ForeignKey('users.id'))
    sum_score: int = Column(Integer)


Base.metadata.create_all(engine)
