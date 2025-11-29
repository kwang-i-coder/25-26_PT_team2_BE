from fastapi import FastAPI
from .routers.auth_router import router as auth_router
from .dependencies.database import Base, engine, get_db
from .models import user_models, post_models
from .routers.platform_router import router as platform_router 
from .routers.jandi_router import router as jandi_router
from .routers.user_router import router as user_router
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router=auth_router)
app.include_router(router=jandi_router)
app.include_router(router=platform_router)
app.include_router(user_router)

get_db()

@app.get("/")
async def root():
    return {"message": "Jandi Main Server is Running!"}
