import logging
import urllib.parse


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from config import get_config


# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

logger = logging.getLogger()


async def connect_db() -> AsyncEngine:
    # try:
    db_cfg = get_config()
    engine = create_async_engine(
        f"postgresql+asyncpg://{db_cfg['db_user']}:{db_cfg['db_password']}@{db_cfg['db_host']}/{db_cfg['db_name']}",
        pool_pre_ping=True
    )
    return engine
    # except Exception as e:
    #     logger.error(f"Failed to connect to MySQL database: {e}")
    #     raise Exception("Failed to connect to MySQL database")


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#

