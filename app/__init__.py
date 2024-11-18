from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models import Base  # A classe Base que contém as tabelas

# Defina a URL do seu banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./ticket_management.db"  # Altere para o caminho correto do seu banco de dados

# Criação do engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Criação do SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para inicializar o banco de dados (criar as tabelas)
def init_db():
    # Criação das tabelas no banco de dados (isso cria todas as tabelas definidas no modelo)
    Base.metadata.create_all(bind=engine)

# Chame a função init_db diretamente no arquivo main.py ou onde for necessário
