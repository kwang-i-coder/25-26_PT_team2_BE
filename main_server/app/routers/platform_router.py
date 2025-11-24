import jwt
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from typing import Optional
import os
from app.dependencies.database import get_db
from app.models.user_models import UserPlatform, Platform, UserPlatformRequest

router = APIRouter(
    prefix="/api/platform",
    tags=["Platform"]
)

SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key")
ALGORITHM = "HS256"

def get_current_user_id(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="인증 헤더가 필요합니다.")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Bearer 스키마가 아닙니다.")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="토큰에 ID가 없습니다.")
            
        return user_id # 여기서는 string 형태의 UUID가 리턴됨

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

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

