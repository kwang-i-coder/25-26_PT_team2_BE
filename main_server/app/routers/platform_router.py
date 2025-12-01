import jwt
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from typing import Optional
import os
from app.dependencies.database import get_db
from app.models.user_models import UserPlatform, Platform, UserPlatformRequest
from app.dependencies.verify_jwt import get_current_user_id

router = APIRouter(
    prefix="/api/platform",
    tags=["Platform"]
)

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
    
    return {
        "message": message
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
