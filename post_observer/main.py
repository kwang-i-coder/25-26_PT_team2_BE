import os
import logging
from dotenv import load_dotenv
from app.services.observer_service import check_new_posts, check_inactive_users

# 환경변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Post Observer 메인 실행 함수 (인프라 크론잡에서 호출)"""
    logger.info("=" * 60)
    logger.info("Post Observer Service Starting...")
    logger.info("=" * 60)

    # 새 글 체크
    logger.info("Running check_new_posts...")
    check_new_posts()

    # 미업로드 사용자 체크
    logger.info("Running check_inactive_users...")
    check_inactive_users()

    logger.info("=" * 60)
    logger.info("Post Observer Service Completed")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()