from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.dependencies import get_db
from app.models import User
from app.services.auth import hash_password

user_router = APIRouter()

@user_router.post("/users/admin/create/")
def create_admin(name: str, email: str, password: str, db: Session = Depends(get_db)):
    # Verificar se o e-mail já está cadastrado
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Criar o administrador
    admin = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        profile="administrador",
        active=True
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    return {"message": "Administrator user created successfully", "user_id": admin.id}
