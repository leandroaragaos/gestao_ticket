import jwt
import datetime
from passlib.context import CryptContext
from fastapi import HTTPException
from app.models import User
from sqlalchemy.orm import Session

# Configurações do JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Inicializa o contexto do passlib para usar o algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funções para gerenciamento de senha
def hash_password(password: str) -> str:
    """
    Função para criptografar a senha do usuário.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Função para verificar se a senha fornecida corresponde à senha criptografada.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Funções para gerenciamento de JWT
def create_access_token(data: dict):
    """
    Função para criar um token JWT com dados de payload.
    O token expira em 1 hora.
    """
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Função para verificar a validade de um token JWT.
    Se o token for inválido ou expirado, gera uma exceção HTTP.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
