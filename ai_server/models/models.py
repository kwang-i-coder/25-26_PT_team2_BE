from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID  # Postgres 전용 UUID 타입
from dependencies.database import Base
import uuid
from datetime import datetime

class Posts(Base):
    __tablename__ = "POSTS"
    url = Column(String, nullable=False, primary_key=True)
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("USER.user_id"), 
        nullable=False, 
        primary_key=True,
    )
    platform_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("PLATFORM.platform_id"), 
        nullable=False, 
        primary_key=True,
    )
    date = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    title = Column(String, nullable=False)

class Platform(Base):
    __tablename__ = "PLATFORM"
    
    platform_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True) 


class User(Base):
    __tablename__ = "USER"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255))
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class POST_AGG(Base):
    __tablename__ = "POST_AGG"
    category = Column(String, nullable=False, primary_key=True)
    date = Column(DateTime, nullable=False, primary_key=True)
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("USER.user_id"), 
        nullable=False, 
        primary_key=True,
    )
    count = Column(Integer, nullable=False)

class UserStat(Base):
    __tablename__ = "USER_STAT"

    user_id = Column(UUID(as_uuid=True), ForeignKey("USER.user_id"), primary_key=True)
    category = Column(String(255), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    count = Column(Integer, default=0)