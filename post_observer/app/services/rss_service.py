from typing import List
from app.models.schemas import ArticleSchema
from app.parsers.naver import NaverRSSParser
from app.parsers.tistory import TistoryRSSParser
from app.parsers.velog import VelogRSSParser
import logging

logger = logging.getLogger(__name__)

# 플랫폼별 파서 매핑
PARSER_MAP = {
    "naver": NaverRSSParser(),
    "tistory": TistoryRSSParser(),
    "velog": VelogRSSParser(),
}

def fetch_rss(platform_name: str, account_id: str) -> List[ArticleSchema]:
    """
    플랫폼별 RSS 수집 및 파싱

    Args:
        platform_name: 플랫폼 이름 (Naver, Tistory, Velog)
        account_id: 플랫폼별 사용자 식별자

    Returns:
        List[ArticleSchema]: 파싱된 글 목록
    """
    parser = PARSER_MAP.get(platform_name)

    if not parser:
        logger.error(f"Unknown platform: {platform_name}")
        return []

    try:
        articles = parser.parse(account_id)
        return articles
    except Exception as e:
        logger.error(f"Failed to fetch RSS for {platform_name}/{account_id}: {e}")
        return []
