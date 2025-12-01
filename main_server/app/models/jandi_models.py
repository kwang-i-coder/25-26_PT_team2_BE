from app.dependencies.database import Base
from pydantic import BaseModel

class GetJandiResponse(BaseModel):
    date: str
    topic: str
    count: int