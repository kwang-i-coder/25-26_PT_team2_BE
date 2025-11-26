from fastapi import FastAPI
from .routers.auth_router import router as auth_router
from .dependencies.database import Base, engine, get_db
from .models import user_models
from .routers.platform_router import router as platform_router 

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=auth_router)

# app.include_router(user_router)
app.include_router(auth_router)
app.include_router(platform_router)
# app.include_router(jandi_router)

get_db()

@app.get("/")
async def root():
    return {"message": "Jandi Main Server is Running!"}
