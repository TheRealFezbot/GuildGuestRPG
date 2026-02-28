from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.constants import ALLOWED_SPECIAL_CHARS

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
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    payload["exp"] = expire
    
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token):
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

def validate_password_strength(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters.")
    if not any(c.isupper() for c in v):
        raise ValueError("Password must include at least 1 uppercase.")
    if not any(c.islower() for c in v):
        raise ValueError("Password must include at least 1 lowercase.")
    if not any(c.isdigit() for c in v):
        raise ValueError("Password must include at least 1 number.")
    if not any(c in ALLOWED_SPECIAL_CHARS for c in v):
        raise ValueError("Password must include at least 1 special character.")
    return v