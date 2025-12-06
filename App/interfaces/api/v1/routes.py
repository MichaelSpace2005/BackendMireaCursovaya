from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.entities.mechanic import GameMechanic
from app.entities.link import EvolutionLink
from app.interfaces.api.v1.schemas import (
    CreateMechanicRequest,
    MechanicResponse,
    CreateLinkRequest,
    LinkResponse,
)
from app.interfaces.api.dependencies import (
    get_mechanic_repository,
    get_link_repository,
)
from app.interfaces.repos.mechanic_repo import IMechanicRepository
from app.interfaces.repos.link_repo import ILinkRepository
from app.use_cases.create_mechanic import CreateMechanicUseCase
from app.use_cases.get_tree import GetMechanicTreeUseCase


router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


# Mechanics -----------------------------------------------------------------
@router.get("/mechanics/", response_model=List[MechanicResponse])
async def list_mechanics(
    mechanic_repo: IMechanicRepository = Depends(get_mechanic_repository),
):
    mechanics = await mechanic_repo.list_all()
    return mechanics


@router.post("/mechanics/", response_model=MechanicResponse, status_code=status.HTTP_201_CREATED)
async def create_mechanic(
    payload: CreateMechanicRequest,
    mechanic_repo: IMechanicRepository = Depends(get_mechanic_repository),
):
    use_case = CreateMechanicUseCase(mechanic_repo)
    mechanic = GameMechanic(
        id=None,
        name=payload.name,
        description=payload.description,
        year=payload.year,
    )
    created = await use_case.execute(mechanic)
    return created


@router.get("/mechanics/{mechanic_id}/tree")
async def get_mechanic_tree(
    mechanic_id: int,
    mechanic_repo: IMechanicRepository = Depends(get_mechanic_repository),
    link_repo: ILinkRepository = Depends(get_link_repository),
):
    use_case = GetMechanicTreeUseCase(mechanic_repo, link_repo)
    try:
        tree = await use_case.execute(mechanic_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return tree


# Links ---------------------------------------------------------------------
@router.get("/mechanics/links", response_model=List[LinkResponse])
async def list_links(
    link_repo: ILinkRepository = Depends(get_link_repository),
):
    links = await link_repo.list_all()
    return links


@router.post("/mechanics/links", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link(
    payload: CreateLinkRequest,
    link_repo: ILinkRepository = Depends(get_link_repository),
):
    link = EvolutionLink(
        id=None,
        from_id=payload.from_id,
        to_id=payload.to_id,
        type=payload.type,
    )
    created = await link_repo.create(link)
    return created
