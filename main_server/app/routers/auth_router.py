# app/routers/auth_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
import jwt
import os
from app.dependencies.database import get_db
from app.internal.email_service import send_verification_email
from app.models.user_models import User, AuthUser
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"



# Pydantic Models : 값을 쿼리가 아닌 json으로 넘겨주기 위해

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


# JWT 생성

def create_access_token(user_id: str):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# 회원가입

@router.post("/signup")
async def signup(data: SignUpRequest, db: Session = Depends(get_db)):
    # 이메일 중복 검사
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다")

    # User 생성
    new_user = User(email=data.email, name=data.name)
    db.add(new_user)
    db.flush()  # user_id 생성됨

    # 비밀번호 해시
    hashed_pw = pwd_context.hash(data.password)

    # 인증용 토큰
    verify_token = jwt.encode(
        {"sub": str(new_user.user_id), "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # AuthUser 생성
    shadow = AuthUser(
        user_id=new_user.user_id,
        email=data.email,
        hashed_password=hashed_pw,
        is_verified=False,
        verification_token=verify_token
    )

    db.add(shadow)
    db.commit()

    # 이메일 인증 발송
    await send_verification_email(data.email, verify_token)

    return {"message": "회원가입 완료! 이메일을 확인해주세요."}


# 이메일 인증 API

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["sub"]
    except(jwt.exceptions.ExpiredSignatureError):
        raise HTTPException(status_code=400, detail="토큰이 만료되었습니다")
    except(jwt.exceptions.InvalidTokenError):
        raise HTTPException(status_code=400, detail="유효하지 않은 토큰입니다")

    shadow = db.query(AuthUser).filter(AuthUser.user_id == user_id).first()

    if not shadow:
        raise HTTPException(status_code=400, detail="인증 정보가 없습니다")

    if shadow.verification_token != token:
        raise HTTPException(status_code=400, detail="토큰이 일치하지 않습니다")

    shadow.is_verified = True
    shadow.verification_token = None
    db.commit()
    db.execute(text('REFRESH MATERIALIZED VIEW "USER_STAT"'))
    db.commit()

    return {"message": "이메일 인증 완료!"}


# 로그인

@router.post("/signin")
def signin(data: SignInRequest, db: Session = Depends(get_db)):

    # 이메일 일치 유저 찾기
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="존재하지 않는 이메일입니다")

    # AuthUser 찾기
    shadow = db.query(AuthUser).filter(AuthUser.user_id == user.user_id).first()
    if not shadow:
        raise HTTPException(status_code=400, detail="인증 정보 없음")

    # 비밀번호 검증
    if not pwd_context.verify(data.password, shadow.hashed_password):
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다")

    # 이메일 인증 체크
    if not shadow.is_verified:
        raise HTTPException(status_code=400, detail="이메일 인증이 필요합니다")
    
    #로그인 성공 시 user테이블의 email에 값 추가
    if user.email != shadow.email:
        user.email = shadow.email
        db.commit()

    # JWT 토큰 발급
    token = jwt.encode(
        {"sub": str(user.user_id), "exp": datetime.utcnow() + timedelta(days=7)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}

