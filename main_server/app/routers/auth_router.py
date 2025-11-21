from fastapi import APIRouter
from app.models.auth_models import SignInRequest, SignInResponse

auth_router = APIRouter(prefix='/auth')

@auth_router.post('/signIn', response_model=SignInResponse)
def sign_in(req: SignInRequest):
    return {"access_token": "example_token"}