from jose import JWTError
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.user import User
from app.core.database import get_db
from app.crud.user import get_user_by_id
from app.core.security import decode_token
from app.crud.character import get_character_by_user_id

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token.")
        
        user = get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(401, "Invalid token.")
        
        return user
    except JWTError:
        raise HTTPException(401, "Invalid token.")
    
def get_current_character(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    character = get_character_by_user_id(db, current_user.id)
    if not character:
        raise HTTPException(status_code=404, detail="No character found")
    
    return character

