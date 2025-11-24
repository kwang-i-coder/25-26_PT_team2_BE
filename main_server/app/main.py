from fastapi import FastAPI
from app.routers.auth_router import auth_router
from app.dependencies.database import Base, engine, get_db
from app.models import user_models
from app.routers.platform_router import router as platform_router 

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
