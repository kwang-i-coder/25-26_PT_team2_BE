import jwt
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import os
from app.dependencies.database import get_db
from app.models.user_models import UserPlatform, Platform, UserPlatformRequest
from app.models.post_models import Posts
from app.dependencies.verify_jwt import get_current_user_id
from app.parsers.velog import VelogRSSParser
from app.parsers.naver import NaverRSSParser
from app.parsers.tistory import TistoryRSSParser
from app.dependencies.rabbitmq import publish_message
import time
router = APIRouter(
    prefix="/api/platform",
    tags=["Platform"]
)

platform_register_map = {
    "velog": VelogRSSParser(),
    "naver": NaverRSSParser(),
    "tistory": TistoryRSSParser()
}

@router.put("")
def register_platform(
    req: UserPlatformRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
    ):
    platform_info = db.query(Platform).filter(Platform.name == req.platform_name).first()
    
    if not platform_info:
        raise HTTPException(status_code=404, detail=f"지원하지 않는 플랫폼: {req.platform_name}")

    existing_mapping = db.query(UserPlatform).filter(
        UserPlatform.user_id == user_id,
        UserPlatform.platform_id == platform_info.platform_id
    ).first()

    # 3. Upsert
    if existing_mapping:
        existing_mapping.account_id = req.account_id
        message = "업데이트 완료"
    else:
        new_mapping = UserPlatform(
            user_id=user_id,
            platform_id=platform_info.platform_id,
            account_id=req.account_id,
            last_upload=None
        )
        db.add(new_mapping)
        message = "등록 완료"

    db.commit()

    articles = platform_register_map[req.platform_name].parse(req.account_id)
    data = []
    for article in articles:
        data.append({
            "link": article.link,
            "published_at": article.published_at,
            "title": article.title,
            "user_id": user_id,
            "platform": req.platform_name
        })

    publish_message("platform_register", data)

    return {
        "message": message
    }

@router.delete("")
def delete_platform(
    req: UserPlatformRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
    ):
    try: 
        platform_info = db.query(Platform).filter(Platform.name == req.platform_name).first()
        
        if not platform_info:
            raise HTTPException(status_code=404, detail=f"지원하지 않는 플랫폼: {req.platform_name}")

        existing_mapping = db.query(UserPlatform).filter(
            UserPlatform.user_id == user_id,
            UserPlatform.platform_id == platform_info.platform_id
        ).first()

        existing_posts = db.query(Posts).filter(
            Posts.user_id == user_id,
            Posts.platform_id == platform_info.platform_id
        ).all()

        if not existing_mapping:
            raise HTTPException(status_code=404, detail="플랫폼이 등록되어 있지 않습니다.")

        for post in existing_posts:
            db.delete(post)
        db.delete(existing_mapping)
        db.commit()
        db.execute(text('REFRESH MATERIALIZED VIEW "USER_STAT"'))
        db.execute(text('REFRESH MATERIALIZED VIEW "POST_AGG"'))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"플랫폼 삭제 중 오류 발생: {e}")

    return {
        "message": "삭제 완료"
    }

@router.get("")
def get_platforms(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
    ):
    user_platforms = db.query(UserPlatform, Platform).filter(UserPlatform.platform_id == Platform.platform_id, UserPlatform.user_id == user_id).all()
    res = []
    for user_platform, platform in user_platforms:
        res.append({
            "platform_name": platform.name,
            "account_id": user_platform.account_id,
            "last_upload": user_platform.last_upload
        })
    return res
