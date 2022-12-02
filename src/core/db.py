from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.core.settings import Settings

Base = declarative_base()

engine = create_engine(Settings.DATABASE_URL)
Session = sessionmaker(engine, expire_on_commit=False)
