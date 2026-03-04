from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date, datetime
from uuid import UUID

from app.core.constants import MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH
from app.core.security import validate_password_strength, validate_name



class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    date_of_birth: date

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        return validate_name(v, MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH, "Username")


    @field_validator("password")
    @classmethod
    def check_password_strength(cls, v):
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
    def check_password_strength(cls, v):
        return validate_password_strength(v)
