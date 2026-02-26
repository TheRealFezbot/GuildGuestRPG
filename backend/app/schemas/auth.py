from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID

class UserRegister(BaseModel):
    email: str
    username: str
    password: str
    date_of_birth: date

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
