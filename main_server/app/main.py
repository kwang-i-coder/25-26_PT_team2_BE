from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.auth_router import router as auth_router
from .dependencies.database import Base, engine, get_db
from .models import user_models, post_models
from .routers.platform_router import router as platform_router 
from .routers.jandi_router import router as jandi_router
from .routers.user_router import router as user_router
from .routers.ui import router as ui_router
Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:3000", # 프론트엔드 URL을 여기에 입력하세요
    "https://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # 쿠키 및 인증 정보 허용
    allow_methods=["*"],    # 모든 HTTP 메서드 허용
    allow_headers=["*"],    # 모든 헤더 허용
)
app.include_router(router=auth_router)
app.include_router(router=jandi_router)
app.include_router(router=platform_router)
app.include_router(user_router)
app.include_router(ui_router)

get_db()

@app.get("/")
async def root():
    return {"message": "Jandi Main Server is Running!"}
