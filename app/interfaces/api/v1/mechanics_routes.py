from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.interfaces.api.v1 import schemas
from app.interfaces.api.dependencies import (
    get_db_session, get_mechanic_repo, get_link_repo, get_current_user
)
from app.use_cases.create_mechanic import CreateMechanicUseCase
from app.use_cases.get_tree import GetMechanicTreeUseCase
from app.entities.mechanic import GameMechanic
from app.entities.link import EvolutionLink

router = APIRouter(prefix="/mechanics", tags=["mechanics"])

@router.post("/", response_model=schemas.MechanicDTO, status_code=201)
async def create_mechanic(
    dto: schemas.MechanicDTO,
    current_user: str = Depends(get_current_user),
    session=Depends(get_db_session)
):
    """Create a new game mechanic (requires authentication)"""
    repo = get_mechanic_repo(session)
    uc = CreateMechanicUseCase(repo)
    try:
        created = await uc.execute(GameMechanic(id=None, name=dto.name, description=dto.description, year=dto.year))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return schemas.MechanicDTO.from_orm(created) if hasattr(created, "__dict__") else created

@router.post("/links", response_model=schemas.LinkDTO, status_code=201)
async def create_link(
    dto: schemas.LinkDTO,
    current_user: str = Depends(get_current_user),
    session=Depends(get_db_session)
):
    """Create a link between two mechanics (requires authentication)"""
    repo = get_link_repo(session)
    # simple validation could be added (existence of mechanic ids)
    created = await repo.create(EvolutionLink(id=None, from_id=dto.from_id, to_id=dto.to_id, type=dto.type))
    return schemas.LinkDTO(**created.__dict__)

@router.get("/{id}/tree", response_model=schemas.TreeResponse)
async def get_tree(
    id: int,
    session=Depends(get_db_session)
):
    """Get evolution tree for a mechanic"""
    mechanic_repo = get_mechanic_repo(session)
    link_repo = get_link_repo(session)
    uc = GetMechanicTreeUseCase(mechanic_repo, link_repo)
    try:
        tree = await uc.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return tree

@router.get("/", response_model=List[schemas.MechanicDTO])
async def list_mechanics(session=Depends(get_db_session)):
    """Get all mechanics"""
    repo = get_mechanic_repo(session)
    mechanics = await repo.list_all()
    return [schemas.MechanicDTO.from_orm(m) if hasattr(m, "__dict__") else m for m in mechanics]

@router.get("/links", response_model=List[schemas.LinkDTO])
async def list_links(session=Depends(get_db_session)):
    """Get all links"""
    repo = get_link_repo(session)
    links = await repo.list_links()
    return [schemas.LinkDTO(**l.__dict__) for l in links]
