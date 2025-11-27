from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ArticleSchema(BaseModel):
    # RSS 피드에서 파싱한 글 정보
    title: str
    link: str
    published_at: datetime
    thumbnail: Optional[str] = None
    tags: Optional[List[str]] = None
