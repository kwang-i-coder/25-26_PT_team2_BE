from fastapi import HTTPException, Header
from typing import Optional
import jwt
import os
import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "my_super_secret_key")
UI_SECRET_KEY = os.getenv("UI_SECRET_KEY", "my_super_secret_key")
ALGORITHM = "HS256"


def get_current_user_id(Authorization: Optional[str] = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=401, detail="인증 헤더가 필요합니다.")
    
    try:
        scheme, token = Authorization.split()
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

def get_jandi_user_id(token: str):
    try:
        if token is None:
            raise HTTPException(status_code=401, detail="인증 헤더가 필요합니다.")
        payload = jwt.decode(token, UI_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="토큰에 ID가 없습니다.")
            
        return user_id # 여기서는 string 형태의 UUID가 리턴됨

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")