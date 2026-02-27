from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime
from uuid import UUID



class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    date_of_birth: date

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if len(v) <8:
            raise ValueError("Password must be at least 8 characters.")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must include at least 1 uppercase.")
        if not any(c.islower() for c in v):
            raise ValueError("Password must include at least 1 lowercase.")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must include at least 1 number.")
        if not any(c in "!@#$%^&*(\{\}\\/><.,\"':;)-_+=?~[]|" for c in v):
            raise ValueError("Password must include at least 1 special character.")
        
        return v
    
class UserLogin(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    username: str
    email: str
    is_verified: bool
    created_at: datetime

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v):
        if len(v) <8:
            raise ValueError("Password must be at least 8 characters.")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must include at least 1 uppercase.")
        if not any(c.islower() for c in v):
            raise ValueError("Password must include at least 1 lowercase.")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must include at least 1 number.")
        if not any(c in "!@#$%^&*(\{\}\\/><.,\"':;)-_+=?~[]|" for c in v):
            raise ValueError("Password must include at least 1 special character.")
        
        return v
