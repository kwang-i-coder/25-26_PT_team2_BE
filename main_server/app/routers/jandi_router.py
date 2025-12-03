from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.verify_jwt import get_current_user_id, get_jandi_user_id
from app.models.jandi_models import GetJandiResponse
from app.models.post_models import POST_AGG
from app.internal.html_template import get_html_template
from datetime import datetime, timedelta
from pydantic import BaseModel

import os
import jwt
import dotenv
router = APIRouter(prefix='/api/jandi')

dotenv.load_dotenv()

UI_SECRET_KEY = os.getenv("UI_SECRET_KEY", "my_super_secret_key")
ALGORITHM = "HS256"

@router.get("/", response_model=list[GetJandiResponse])
async def get_jandi(date: str | None = None,db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    # date가 없으면 오늘 날짜로 설정
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    date: datetime = datetime.strptime(date, "%Y-%m-%d")
    # user_id로 POST_AGG 테이블에서 데이터를 가져옴
    posts: list[POST_AGG] = db.query(POST_AGG).filter(POST_AGG.user_id == user_id, POST_AGG.date.between(date-timedelta(days=30), date)).all()
    if len(posts) == 0:
        return []
    # 그걸 [GetJandiResponse]로 변환
    response = [GetJandiResponse(date=post.date.strftime("%Y-%m-%d"), topic=post.category, count=post.count) for post in posts]
    return response

class GetSignedUrlRequest(BaseModel):
    url: str

@router.get("/signedUrl", response_model=GetSignedUrlRequest)
async def get_signed_url(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="인증 헤더가 필요합니다.")
    verify_token = jwt.encode(
        {"sub": str(user_id)},
        UI_SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"url": f"http://136.110.239.66/api/jandi/widget?token={verify_token}"}


@router.get("/widget")
def get_jandi(db: Session = Depends(get_db), token: str|None = None):
    if token is None:
        raise HTTPException(status_code=401, detail="인증 헤더가 필요합니다.")
    user_id = get_jandi_user_id(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="인증 헤더가 필요합니다.")
    
    date = datetime.now()
    # user_id로 POST_AGG 테이블에서 데이터를 가져옴
    posts: list[POST_AGG] = db.query(POST_AGG).filter(POST_AGG.user_id == user_id, POST_AGG.date.between(date-timedelta(days=30), date)).all()
    if len(posts) == 0:
        return []
    # 그걸 [GetJandiResponse]로 변환
    response = [{"date": post.date.strftime("%Y-%m-%d"), "topic": post.category, "count": post.count} for post in posts]

    
    return HTMLResponse(content=get_html_template(response), status_code=200)