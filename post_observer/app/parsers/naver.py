from datetime import datetime
from app.parsers.base import BaseRSSParser
from app.models.schemas import ArticleSchema

class NaverRSSParser(BaseRSSParser):
    """네이버 블로그 RSS 파서"""

    def get_rss_url(self, account_id: str) -> str:
        """
        네이버 블로그 RSS URL 생성

        Args:
            account_id: 네이버 블로그 ID

        Returns:
            https://rss.blog.naver.com/{blogId}.xml
        """
        return f"https://rss.blog.naver.com/{account_id}.xml"

    def normalize(self, entry) -> ArticleSchema:
        """
        네이버 RSS 엔트리를 ArticleSchema로 변환

        Args:
            entry: feedparser entry object

        Returns:
            ArticleSchema
        """
        # 발행 시간 파싱
        published_at = datetime(*entry.published_parsed[:6])

        # 썸네일 추출 (있으면)
        thumbnail = None
        if hasattr(entry, 'media_content') and entry.media_content:
            thumbnail = entry.media_content[0].get('url')

        # 태그 추출 (있으면)
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
