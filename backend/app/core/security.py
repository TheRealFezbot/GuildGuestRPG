from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def validate_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_access_token(data):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload["exp"] = expire
    
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(data):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload["exp"] = expire
    
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token):
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])