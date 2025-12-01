from abc import ABC, abstractmethod
from typing import List
import feedparser
import httpx
from datetime import datetime
import logging
from app.models.schemas import ArticleSchema

logger = logging.getLogger(__name__)

class BaseRSSParser(ABC):

    @abstractmethod
    def get_rss_url(self, account_id: str) -> str:
        """
        플랫폼별 RSS URL 생성

        Args:
            account_id: 플랫폼별 사용자 식별자 (blogId, username 등)

        Returns:
            RSS feed URL
        """
        pass

    @abstractmethod
    def normalize(self, entry) -> ArticleSchema:
        """
        RSS 엔트리를 ArticleSchema로 변환

        Args:
            entry: feedparser entry object

        Returns:
            ArticleSchema instance
        """
        pass

    def parse(self, account_id: str) -> List[ArticleSchema]:
        """
        RSS 피드를 파싱하여 ArticleSchema 리스트 반환 (공통 로직)

        Args:
            account_id: 플랫폼별 사용자 식별자

        Returns:
            List of ArticleSchema
        """
        try:
            rss_url = self.get_rss_url(account_id)
            logger.info(f"Fetching RSS from: {rss_url}")

            # HTTP 요청으로 RSS 가져오기
            response = httpx.get(rss_url, timeout=10.0)
            response.raise_for_status()

            # feedparser로 파싱
            feed = feedparser.parse(response.content)

            if not feed.entries:
                logger.warning(f"No entries found in RSS feed: {rss_url}")
                return []

            # 각 엔트리를 ArticleSchema로 변환
            articles = []
            for entry in feed.entries:
                try:
                    article = self.normalize(entry)
                    articles.append(article)
                except Exception as e:
                    logger.error(f"Failed to normalize entry: {e}")
                    continue

            logger.info(f"Parsed {len(articles)} articles from {rss_url}")
            return articles

        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching RSS from {account_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error parsing RSS from {account_id}: {e}")
            return []
