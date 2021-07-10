from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI
    #, connect_args={"check_same_thread": False}
    , **Config.SQLALCHEMY_ENGINE_OPTIONS
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()