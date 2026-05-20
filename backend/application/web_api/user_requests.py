from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
import os

from datetime import datetime, timedelta
from backend.application.backend_api import BackendAPI
from backend.infrastructure.dependencies import get_api, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])




# --- Schemas ---
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


# --- Endpoints ---
@router.post("/register")
def register_user(body: RegisterRequest,
                  api: BackendAPI = Depends(get_api)):
    result = api.register_user(body.name, body.email, body.password)
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"id": result.obj}


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
               api: BackendAPI = Depends(get_api)):

    result = api.login_user(form_data.username, form_data.password)
    if not result.successful:
        raise HTTPException(status_code=401, detail=result.info)

    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY no está definida en las variables de entorno")
    
    token = jwt.encode({
        "user_id": result.obj,
        "exp": datetime.utcnow() + timedelta(days=7) # expira en 7 días
        }, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_me(user_id: int = Depends(get_current_user)):
    return {"user_id": user_id}