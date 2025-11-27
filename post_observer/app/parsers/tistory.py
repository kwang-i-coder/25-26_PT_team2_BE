from datetime import datetime
from app.parsers.base import BaseRSSParser
from app.models.schemas import ArticleSchema

class TistoryRSSParser(BaseRSSParser):
    """티스토리 RSS 파서"""

    def get_rss_url(self, account_id: str) -> str:
        """
        티스토리 RSS URL 생성

        Args:
            account_id: 티스토리 블로그 ID

        Returns:
            https://{blogId}.tistory.com/rss
        """
        return f"https://{account_id}.tistory.com/rss"

    def normalize(self, entry) -> ArticleSchema:
        """
        티스토리 RSS 엔트리를 ArticleSchema로 변환

        Args:
            entry: feedparser entry object

        Returns:
            ArticleSchema
        """
        # 발행 시간 파싱
        published_at = datetime(*entry.published_parsed[:6])

        # 썸네일 추출
        thumbnail = None
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            thumbnail = entry.media_thumbnail[0].get('url')

        # 카테고리를 태그로 사용
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
