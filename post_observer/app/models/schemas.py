from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID

class ArticleSchema(BaseModel):
    # RSS 피드에서 파싱한 글 정보
    title: str
    link: str
    published_at: datetime
    thumbnail: Optional[str] = None
    tags: Optional[List[str]] = None

class NewPostMessageSchema(BaseModel):
    # RabbitMQ 메시지 스키마 (새 글 발견 시 발행)
    user_id: str
    platform: str
    article: ArticleSchema
