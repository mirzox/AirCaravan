from typing import Optional, Any
import logging

from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    ForeignKey,
    DateTime,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker


from database import Base

logger = logging.getLogger()


from uuid import UUID, uuid4


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, index=True)
    username = Column("username", String(256), nullable=False)
    full_name = Column("full_name", String(256), nullable=True)
    email = Column("email", String(256), nullable=True)
    is_active = Column("is_active", Integer, nullable=False, default=1)
    user_type = Column("user_type", String(256), nullable=False)
    password = Column("password", String(256), nullable=False)

    def __init__(self, username, email, is_active, user_type, **kw: Any):
        super().__init__(**kw)
        self.username = username
        self.email = email
        self.is_active = is_active
        self.user_type = user_type
