from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID  # Postgres 전용 UUID 타입
from app.dependencies.database import Base
import uuid


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