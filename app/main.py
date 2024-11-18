from fastapi import FastAPI
from app.routes.auth import auth_router
from app.routes.problems import problem_router
from app import init_db  # Importe a função init_db
from app.models import Base
from app.__init__ import engine

init_db()  # Chama a função para criar as tabelas

from app.routes.users import user_router

app = FastAPI()

# Criação das tabelas no banco de dados (se ainda não existirem)
Base.metadata.create_all(bind=engine)

# Incluindo as rotas de usuários
app.include_router(user_router, prefix="/api", tags=["Users"])

# Incluindo as rotas de autenticação
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

# Incluindo as rotas de tipos de problemas
app.include_router(problem_router, prefix="/api/problems", tags=["Problem Types"])
