from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.verify_jwt import get_current_user_id, get_jandi_user_id
from app.models.post_models import POST_AGG
from app.models.jandi_models import GetJandiResponse
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from app.internal.html_template import get_html_template
from datetime import datetime, timedelta
router = APIRouter(prefix='/jandi')


@router.get("/")
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