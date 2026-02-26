from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.core.security import hash_password, validate_password, create_access_token, create_refresh_token, decode_token
from app.schemas.auth import UserRegister, UserLogin, TokenRefresh, TokenResponse, UserResponse
from app.crud.user import get_user_by_email, get_user_by_username, create_user
from app.core.dependencies import get_current_user
from app.core.database import get_db


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(data: UserRegister, db: Session = Depends(get_db)):
    today = date.today()
    age = today.year - data.date_of_birth.year - ((today.month, today.day) < (data.date_of_birth.month, data.date_of_birth.day))

    if age < 13:
        raise HTTPException(status_code=400, detail="You must be at least 13 years old to register.")
    
    if get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="That email already exists.")
    
    if get_user_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="That username is taken.")
    
    hashed_password = hash_password(data.password)

    create_user(db, data.email, data.username, hashed_password)

    return {"message": "Registration successful. Please verify your email."}



@router.post("/login")
async def login(data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email) or get_user_by_username(db, data.username)
    validated = user and validate_password(data.password, user.hashed_password)
    
    if not validated:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)    



@router.post("/refresh")
async def refresh(data: TokenRefresh):
    try:
        payload = decode_token(data.refresh_token)
        access_token = create_access_token({"sub": payload["sub"]})
        refresh_token = create_refresh_token({"sub": payload["sub"]})
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return current_user