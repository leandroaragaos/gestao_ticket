from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import verify_token
from app.models import User



def get_current_user(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    """
    Obtém o usuário atual com base no token JWT.
    """
    email = token.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
