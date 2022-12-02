from src.core.db import Base, engine, Session


def get_database() -> Session:
    session = Session()

    try:
        yield session
    finally:
        session.close()
