from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from passlib.hash import bcrypt

Base = declarative_base()

# Modelo de Franchises
class Franchise(Base):
    __tablename__ = "franchises"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    condominiums = relationship("Condominium", back_populates="franchise")

# Modelo de Condominiums
class Condominium(Base):
    __tablename__ = "condominiums"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    franchise_id = Column(Integer, ForeignKey("franchises.id"))

    franchise = relationship("Franchise", back_populates="condominiums")

# Modelo de Users
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    profile = Column(String, nullable=False)  # suporte, sindico, administrador
    franchise_id = Column(Integer, ForeignKey("franchises.id"))
    active = Column(Boolean, default=True)

    franchise = relationship("Franchise")

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

# Modelo de Problem Types
class ProblemType(Base):
    __tablename__ = "problem_types"  # Nome da tabela no banco de dados
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
