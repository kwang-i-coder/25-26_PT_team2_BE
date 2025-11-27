from typing import List
from sqlalchemy.orm import Session
from app.models.db_models import UserPlatform, Platform
from app.dependencies.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

class UserPlatformInfo:
    """사용자-플랫폼 정보 DTO"""
    def __init__(self, user_id, platform_name, account_id, last_upload):
        self.user_id = user_id
        self.platform_name = platform_name
        self.account_id = account_id
        self.last_upload = last_upload

    def __repr__(self):
        return f"UserPlatformInfo(user_id={self.user_id}, platform={self.platform_name}, account_id={self.account_id})"

def get_all_user_platforms() -> List[UserPlatformInfo]:
    """
    DB에서 모든 사용자-플랫폼 정보 조회

    Returns:
        List[UserPlatformInfo]: 사용자-플랫폼 정보 리스트
    """
    db = SessionLocal()
    try:
        # USER_PLATFORM과 PLATFORM JOIN
        results = db.query(
            UserPlatform.user_id,
            Platform.name.label('platform_name'),
            UserPlatform.account_id,
            UserPlatform.last_upload
        ).join(
            Platform, UserPlatform.platform_id == Platform.platform_id
        ).all()

        user_platforms = [
            UserPlatformInfo(
                user_id=row.user_id,
                platform_name=row.platform_name,
                account_id=row.account_id,
                last_upload=row.last_upload
            )
            for row in results
        ]

        logger.info(f"Found {len(user_platforms)} user-platform mappings")
        return user_platforms

    except Exception as e:
        logger.error(f"Failed to fetch user platforms: {e}")
        return []
    finally:
        db.close()

def update_last_upload(user_id, platform_name: str, last_upload_time):
    """
    사용자-플랫폼의 last_upload 시각 업데이트

    Args:
        user_id: 사용자 ID
        platform_name: 플랫폼 이름
        last_upload_time: 마지막 업로드 시각
    """
    db = SessionLocal()
    try:
        # Platform ID 조회
        platform = db.query(Platform).filter(Platform.name == platform_name).first()
        if not platform:
            logger.error(f"Platform not found: {platform_name}")
            return

        # UserPlatform 업데이트
        user_platform = db.query(UserPlatform).filter(
            UserPlatform.user_id == user_id,
            UserPlatform.platform_id == platform.platform_id
        ).first()

        if user_platform:
            user_platform.last_upload = last_upload_time
            db.commit()
            logger.info(f"Updated last_upload for user {user_id}, platform {platform_name}")
        else:
            logger.error(f"UserPlatform not found: user={user_id}, platform={platform_name}")

    except Exception as e:
        logger.error(f"Failed to update last_upload: {e}")
        db.rollback()
    finally:
        db.close()
