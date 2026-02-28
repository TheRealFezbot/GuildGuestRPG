from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from jose import JWTError

from app.crud.user import get_user_by_email, get_user_by_username, create_user, get_user_by_id, verify_user, delete_user, update_password
from app.schemas.auth import UserRegister, UserLogin, TokenRefresh, TokenResponse, UserResponse, PasswordReset, PasswordResetRequest
from app.core.security import hash_password, validate_password, create_access_token, create_refresh_token, decode_token
from app.services.email import send_verification_email, send_reset_email
from app.core.dependencies import get_current_user
from app.core.constants import MIN_AGE
from app.core.database import get_db


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(data: UserRegister, db: Session = Depends(get_db)):
    today = date.today()
    age = today.year - data.date_of_birth.year - ((today.month, today.day) < (data.date_of_birth.month, data.date_of_birth.day))

    if age < MIN_AGE:
        raise HTTPException(status_code=400, detail="You must be at least 13 years old to register.")
    
    if get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="That email already exists.")
    
    if get_user_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="That username is taken.")
    
    hashed_password = hash_password(data.password)
    user = create_user(db, data.email, data.username, hashed_password)

    access_token = create_access_token({"sub": str(user.id), "type": "verify"})
    try:
        send_verification_email(user.email, access_token)
        return {"message": "Registration successful. Please verify your email."}
    except Exception:
        delete_user(db, user)
        raise HTTPException(status_code=400, detail="Something went wrong. Please check if your email is correct.")


@router.get("/verify")
async def verify(token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    if not payload.get("type") == "verify":
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = get_user_by_id(db, payload["sub"])
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    verify_user(db, user)
    return {"message": "Email verified successfully."}


@router.post("/login")
async def login(data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email) or get_user_by_username(db, data.username)
    validated = user and validate_password(data.password, user.hashed_password)
    
    if not validated:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email.")
    if user.is_banned:
        raise HTTPException(status_code=403, detail=f"You are banned. Reason: {user.ban_reason}")
    
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
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return current_user


@router.post("/forgot-password")
async def forgot_password(data: PasswordResetRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    
    if user:
        token = create_access_token({"sub": str(user.id), "type": "reset"})
        send_reset_email(user.email, token)

    return {"message": "If that email exists, you'll receive a reset link"}


@router.post("/reset-password")
async def reset_password(data: PasswordReset, db: Session = Depends(get_db)):
    try:
        payload = decode_token(data.token)
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    if not payload.get("type") == "reset":
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = get_user_by_id(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    new_hashed_password = hash_password(data.new_password)

    update_password(db, user, new_hashed_password)

    return {"message": "Password reset, please login."}