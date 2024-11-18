from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import ProblemType
from app.services.dependencies import get_db, get_current_user

problem_router = APIRouter()

@problem_router.post("/")
def create_problem_type(
    name: str,
    description: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verificar se o usuário é administrador
    if current_user.get("profile") != "administrador":
        raise HTTPException(status_code=403, detail="Permission denied")

    # Verificar se o tipo de problema já existe
    existing_problem = db.query(ProblemType).filter(ProblemType.name == name).first()
    if existing_problem:
        raise HTTPException(status_code=400, detail="Problem type already exists")

    # Criar o novo tipo de problema
    problem_type = ProblemType(name=name, description=description)
    db.add(problem_type)
    db.commit()
    db.refresh(problem_type)

    return {"message": "Problem type created successfully", "id": problem_type.id}


@problem_router.get("/")
def list_problem_types(db: Session = Depends(get_db)):
    problem_types = db.query(ProblemType).all()
    return problem_types


@problem_router.put("/{problem_type_id}")
def update_problem_type(
    problem_type_id: int,
    name: str = None,
    description: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verificar se o usuário é administrador
    if current_user.get("profile") != "administrador":
        raise HTTPException(status_code=403, detail="Permission denied")

    # Buscar o tipo de problema
    problem_type = db.query(ProblemType).filter(ProblemType.id == problem_type_id).first()
    if not problem_type:
        raise HTTPException(status_code=404, detail="Problem type not found")

    # Atualizar os dados
    if name:
        problem_type.name = name
    if description:
        problem_type.description = description

    db.commit()
    db.refresh(problem_type)

    return {"message": "Problem type updated successfully", "id": problem_type.id}


@problem_router.delete("/{problem_type_id}")
def delete_problem_type(
    problem_type_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Verificar se o usuário é administrador
    if current_user.get("profile") != "administrador":
        raise HTTPException(status_code=403, detail="Permission denied")

    # Buscar e remover o tipo de problema
    problem_type = db.query(ProblemType).filter(ProblemType.id == problem_type_id).first()
    if not problem_type:
        raise HTTPException(status_code=404, detail="Problem type not found")

    db.delete(problem_type)
    db.commit()

    return {"message": "Problem type deleted successfully"}
