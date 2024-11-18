from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth import create_access_token
from app.models import User
from app.__init__ import SessionLocal

auth_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Endpoint para autenticação de usuários.
    """
    # Busca o usuário no banco de dados pelo email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Verifica se a senha está correta
    if not user.check_password(password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Gera o token JWT com informações do usuário
    token = create_access_token({"sub": user.email, "profile": user.profile})
    return {"access_token": token, "token_type": "bearer"}
