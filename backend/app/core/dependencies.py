from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from app.core.security import decode_token
from app.crud.user import get_user_by_id
from jose import JWTError

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
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

