from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime
from uuid import UUID
from app.core.security import validate_password_strength



class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    date_of_birth: date

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        return validate_password_strength(v)
    
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
        return validate_password_strength(v)
