from fastapi import APIRouter
from app.interfaces.api.v1.auth_routes import router as auth_router
from app.interfaces.api.v1 import mechanics_routes

router = APIRouter()

# Include sub-routers
router.include_router(auth_router)
router.include_router(mechanics_routes.router)

@router.post("/mechanics", response_model=schemas.MechanicDTO, status_code=201)
async def create_mechanic(dto: schemas.MechanicDTO, session=Depends(get_db_session)):
    repo = get_mechanic_repo(session)
    uc = CreateMechanicUseCase(repo)
    try:
        created = await uc.execute(GameMechanic(id=None, name=dto.name, description=dto.description, year=dto.year))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return schemas.MechanicDTO.from_orm(created) if hasattr(created, "__dict__") else created

@router.post("/links", response_model=schemas.LinkDTO, status_code=201)
async def create_link(dto: schemas.LinkDTO, session=Depends(get_db_session)):
    repo = get_link_repo(session)
    # simple validation could be added (existence of mechanic ids)
    created = await repo.create(EvolutionLink(id=None, from_id=dto.from_id, to_id=dto.to_id, type=dto.type))
    return schemas.LinkDTO(**created.__dict__)

@router.get("/mechanics/{id}/tree", response_model=schemas.TreeResponse)
async def get_tree(id: int, session=Depends(get_db_session)):
    mechanic_repo = get_mechanic_repo(session)
    link_repo = get_link_repo(session)
    uc = GetMechanicTreeUseCase(mechanic_repo, link_repo)
    try:
        tree = await uc.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return tree