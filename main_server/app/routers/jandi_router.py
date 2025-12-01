from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.verify_jwt import get_current_user_id
from app.models.jandi_models import GetJandiResponse
from app.models.post_models import POST_AGG
from datetime import datetime, timedelta
router = APIRouter(prefix='/api/jandi')

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