from fastapi import FastAPI
from app.routers.auth_router import auth_router

app = FastAPI()
app.include_router(router=auth_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}