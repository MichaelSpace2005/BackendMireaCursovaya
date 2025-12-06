from fastapi import APIRouter, Depends, HTTPException

from app.interfaces.api.v1 import auth_schemas
from app.interfaces.api.dependencies import (
    get_db_session,
    get_user_repo,
    get_email_token_repo,
    get_current_user,
)
from app.use_cases.auth import RegisterUserUseCase, VerifyEmailUseCase, AuthenticateUserUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=auth_schemas.RegisterResponse, status_code=201)
async def register(
    request: auth_schemas.UserRegisterRequest,
    session=Depends(get_db_session),
):
    """Register new user"""
    user_repo = get_user_repo(session)
    email_token_repo = get_email_token_repo(session)

    uc = RegisterUserUseCase(user_repo, email_token_repo)
    try:
        user, token = await uc.execute(request.email, request.username, request.password)
        verification_link = f"http://localhost:8000/verify-email?token={token.token}"
        print(f"Verification link: {verification_link}")  # For testing
        return auth_schemas.RegisterResponse(
            message=f"Registration successful. Verification link sent to {user.email}",
            email=user.email,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/verify-email", response_model=auth_schemas.UserDTO)
async def verify_email(
    request: auth_schemas.VerifyEmailRequest,
    session=Depends(get_db_session),
):
    """Verify email with token"""
    user_repo = get_user_repo(session)
    email_token_repo = get_email_token_repo(session)

    uc = VerifyEmailUseCase(user_repo, email_token_repo)
    try:
        user = await uc.execute(request.token)
        return auth_schemas.UserDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            is_verified=user.is_verified,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login", response_model=auth_schemas.TokenResponse)
async def login(
    request: auth_schemas.UserLoginRequest,
    session=Depends(get_db_session),
):
    """Login user"""
    user_repo = get_user_repo(session)

    uc = AuthenticateUserUseCase(user_repo)
    try:
        user, token = await uc.execute(request.email, request.password)
        return auth_schemas.TokenResponse(
            access_token=token,
            user=auth_schemas.UserDTO(
                id=user.id,
                email=user.email,
                username=user.username,
                is_verified=user.is_verified,
            ),
        )
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))


@router.get("/me", response_model=auth_schemas.UserDTO)
async def get_current_user_info(
    current_user_email: str = Depends(get_current_user),
    session=Depends(get_db_session),
):
    """Get current authenticated user"""
    user_repo = get_user_repo(session)
    user = await user_repo.get_by_email(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return auth_schemas.UserDTO(
        id=user.id,
        email=user.email,
        username=user.username,
        is_verified=user.is_verified,
    )
