from datetime import datetime
from app.services import platform_service, rss_service
# from app.dependencies.rabbitmq import publish_message  # RabbitMQ 발행용 (구현 필요)
import logging

logger = logging.getLogger(__name__)

def check_new_posts():
    """
    메인 비즈니스 로직: 모든 사용자-플랫폼에 대해 새 글 확인

    작업 흐름:
    1. DB에서 모든 사용자-플랫폼 정보 조회
    2. 각 플랫폼별 RSS 수집
    3. 마지막 업로드 시각과 비교하여 새 글 필터링
    4. 새 글이 있으면 로그 출력 # RabbitMQ 발행 구현 해야함
    5. last_upload 업데이트
    """
    logger.info("=== Starting new posts check ===")

    # 모든 사용자-플랫폼 정보 조회
    user_platforms = platform_service.get_all_user_platforms()

    if not user_platforms:
        logger.info("No user platforms found")
        return

    total_new_posts = 0

    # 각 사용자-플랫폼에 대해 처리
    for up in user_platforms:
        logger.info(f"Checking {up.platform_name} for user {up.user_id} (account: {up.account_id})")

        # RSS 수집
        articles = rss_service.fetch_rss(up.platform_name, up.account_id)

        if not articles:
            logger.info(f"No articles found for {up.platform_name}/{up.account_id}")
            continue

        # 새 글 필터링
        new_articles = []
        latest_published_at = None

        for article in articles:
            # last_upload가 None이면 모든 글이 새 글
            if up.last_upload is None or article.published_at > up.last_upload:
                new_articles.append(article)

                # 가장 최신 발행 시각 추적
                if latest_published_at is None or article.published_at > latest_published_at:
                    latest_published_at = article.published_at

        if not new_articles:
            logger.info(f"No new posts for {up.platform_name}/{up.account_id}")
            continue

        logger.info(f"Found {len(new_articles)} new posts for {up.platform_name}/{up.account_id}")

        # 새 글 발견 시 로그 출력 (RabbitMQ 발행)
        for article in new_articles:
            logger.info(f"  - New post: {article.title} ({article.published_at})")
            # 구현 continue
            total_new_posts += 1

        # last_upload 업데이트 (가장 최신 글의 발행 시각으로)
        if latest_published_at:
            platform_service.update_last_upload(
                user_id=up.user_id,
                platform_name=up.platform_name,
                last_upload_time=latest_published_at
            )

    logger.info(f"=== Finished check: {total_new_posts} new posts found ===")
    # RabbitMQ 발행
