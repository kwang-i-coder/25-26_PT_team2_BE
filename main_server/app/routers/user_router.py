from fastapi import APIRouter, Depends,HttpException
from typing import List
from sqlalchemy.orm import Session 
from app.dependencies.database import get_db
from app.dependencies.verify_jwt import get_current_user_id
from app.models.user_models import UserStat, UserStatResponse, Platform
from app.models.post_models import Post, Posts
from datetime import datetime, date

router = APIRouter(prefix='/api/user')

@router.get("/stats", response_model=UserStatResponse)
def get_user_stats(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    user_stats: List[UserStat] = db.query(UserStat).filter(UserStat.user_id == user_id).all()
    if user_stats is None:
        raise HTTPException(status_code=404, detail="User stats not found")
    elif len(user_stats) == 0:
        raise HTTPException(status_code=404, detail="User stats not found")
    else:
        return UserStatResponse(
            duration= (date.today() - user_stats[0].created_at).days,
            category= [{"category": stat.category, "count": stat.count} for stat in user_stats] if user_stats[0].category is not None else [],
            created_at=user_stats[0].created_at,
            count=sum(stat.count for stat in user_stats)
        )

@router.get("/posts", response_model=list[Post])
def get_user_posts(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
    category: str | None = None
):
    if category is None:
        posts: list[Post] = db.query(Posts, Platform).filter(Posts.user_id == user_id, Posts.platform_id == Platform.platform_id).all()
    else:
        posts: list[Post] = db.query(Posts, Platform).filter(Posts.user_id == user_id, Posts.category == category, Posts.platform_id == Platform.platform_id).all()
    return map(lambda row: Post(url=row[0].url, category=row[0].category, date=row[0].date.strftime("%Y-%m-%d"), title=row[0].title, platform=row[1].name), posts)
