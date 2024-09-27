import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config.database import connectionString as srcConnectionString
from test.config.database import connectionString as testConnectionString

TEST = False

def get_connectionString():
    if TEST:
        return testConnectionString
    return srcConnectionString


engine = create_engine(get_connectionString(), echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()