import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID  # Postgres 전용 UUID 타입
from app.dependencies.database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "USER"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255))
    name = Column(String(255))

class Platform(Base):
    __tablename__ = "PLATFORM"
    
    platform_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True)  

class UserPlatform(Base):
    __tablename__ = "USER_PLATFORM"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("USER.user_id"), primary_key=True)
    platform_id = Column(UUID(as_uuid=True), ForeignKey("PLATFORM.platform_id"), primary_key=True)
    
    account_id = Column("id", String(255)) 
    last_upload = Column(DateTime, nullable=True)

class UserPlatformRequest(BaseModel):
    platform_name: str
    account_id: str
class UserPlatformResponse(BaseModel):
    status: str
    message: str
    platform: str
    registered_id: str

class AuthUser(Base):
    __tablename__ = "AUTH_USER"

    auth_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("USER.user_id"), nullable=False)

    email = Column(String(255), nullable=False)
    hashed_password = Column(String, nullable=False)

    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
