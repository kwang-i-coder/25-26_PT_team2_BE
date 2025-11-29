from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from app.dependencies.database import get_db
from app.dependencies.verify_jwt import get_current_user_id
from app.models.user_models import UserStat, UserStatResponse
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
