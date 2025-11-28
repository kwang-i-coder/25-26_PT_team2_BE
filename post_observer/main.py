import os
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
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
    """Post Observer 메인 실행 함수"""
    logger.info("=" * 60)
    logger.info("🚀 Post Observer Service Starting...")
    logger.info("=" * 60)

    # 스케줄러 생성
    scheduler = BlockingScheduler()

    # 작업 등록
    # 새 글 체크: 매일 오전 10시
    scheduler.add_job(
        check_new_posts,
        trigger='cron',
        hour=10,
        minute=0,
        id='check_new_posts',
        name='Check new blog posts'
    )

    # 미업로드 사용자 체크: 매일 오전 10시
    scheduler.add_job(
        check_inactive_users,
        trigger='cron',
        hour=10,
        minute=0,
        id='check_inactive_users',
        name='Check inactive users'
    )

    # 등록된 작업 출력
    logger.info("Scheduled jobs:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.name} (ID: {job.id}): {job.trigger}")

    logger.info("=" * 60)
    logger.info("Scheduler started. Waiting for scheduled time...")
    logger.info("=" * 60)

    try:
        # 스케줄러 시작 (블로킹)
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("=" * 60)
        logger.info("Post Observer Service Stopping...")
        logger.info("=" * 60)
        scheduler.shutdown()

if __name__ == "__main__":
    main()
