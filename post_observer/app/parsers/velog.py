from datetime import datetime
from app.parsers.base import BaseRSSParser
from app.models.schemas import ArticleSchema

class VelogRSSParser(BaseRSSParser):
    """Velog RSS 파서"""

    def get_rss_url(self, account_id: str) -> str:
        """
        Velog RSS URL 생성

        Args:
            account_id: Velog username

        Returns:
            https://v2.velog.io/rss/@{username}
        """
        return f"https://v2.velog.io/rss/@{account_id}"

    def normalize(self, entry) -> ArticleSchema:
        """
        Velog RSS 엔트리를 ArticleSchema로 변환

        Args:
            entry: feedparser entry object

        Returns:
            ArticleSchema
        """
        # 발행 시간 파싱
        published_at = datetime(*entry.published_parsed[:6])

        # 썸네일 추출
        thumbnail = None
        if hasattr(entry, 'media_content') and entry.media_content:
            thumbnail = entry.media_content[0].get('url')

        # 태그 추출
        tags = None
        if hasattr(entry, 'tags') and entry.tags:
            tags = [tag.term for tag in entry.tags]

        return ArticleSchema(
            title=entry.title,
            link=entry.link,
            published_at=published_at,
            thumbnail=thumbnail,
            tags=tags
        )
