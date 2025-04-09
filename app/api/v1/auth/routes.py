from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token

from app.db.database import get_db
from app.utils import jwt_helpers
from app.utils.google_oauth import oauth
from app.core.config import settings
from app.core.dependencies.security import get_current_user

from app.api.v1.auth import schemas
from app.api.services.user import UserService
from app.api.models.user import User


auth = APIRouter(prefix="/auth", tags=["Authentication"])


@auth.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AuthResponse,
    summary="Create a new user account",
    description="This endpoint takes in the user creation details and returns jwt tokens along with user data",
    tags=["Authentication"],
)
def register(
    schema: schemas.RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """Endpoint for a user to register their account

    Args:
    schema (schemas.LoginRequest): Login request schema
    db (Annotated[Session, Depends): Database session
    """

    # Create user account
    service = UserService(db=db)

    user = service.register(schema=schema)

    # Create access and refresh tokens
    access_token = jwt_helpers.create_jwt_token("access", user.id)
    refresh_token = jwt_helpers.create_jwt_token("refresh", user.id)

    response_data = schemas.AuthResponseData(id=user.id, username=user.username)

    return schemas.AuthResponse(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        access_token=access_token,
        refresh_token=refresh_token,
        data=response_data,
    )


@auth.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AuthResponse,
    summary="Login a registered user",
    description="This endpoint retrieves the jwt tokens for a registered user",
    tags=["Authentication"],
)
def login(
    schema: schemas.LoginRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """Endpoint for user login

    Args:
        schema (schemas.LoginRequest): Login request schema
        db (Annotated[Session, Depends): Database session
    """

    # user = services.authenticate(db=db, schema=schema)
    service = UserService(db=db)
    user = service.authenticate(schema=schema)

    # Create access and refresh tokens
    access_token = jwt_helpers.create_jwt_token("access", user.id)
    refresh_token = jwt_helpers.create_jwt_token("refresh", user.id)

    response_data = schemas.AuthResponseData(id=user.id, username=user.username)

    return schemas.AuthResponse(
        status_code=status.HTTP_201_CREATED,
        message="User logged in successfully",
        access_token=access_token,
        refresh_token=refresh_token,
        data=response_data,
    )


@auth.post(
    path="/token/refresh",
    response_model=schemas.TokenRefreshResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh tokens",
    description="This endpoint uses the current refresh token to create new access and refresh tokens",
    tags=["Authentication"],
)
def refresh_token(schema: schemas.TokenRefreshRequest):
    """Endpoint to refresh the access token

    Args:
        schema (schemas.TokenRefreshRequest): Refresh Token Schema

    Returns:
        _type_: Refresh Token Response
    """
    token = jwt_helpers.refresh_access_token(refresh_token=schema.refresh_token)

    return schemas.TokenRefreshResponse(
        status_code=status.HTTP_200_OK,
        message="Access token refreshed successfully",
        access_token=token,
    )


@auth.get(
    path="/google",
    summary="Google OAuth2 Login",
    description="This endpoint redirects to Google for OAuth2 login",
    tags=["Authentication"],
)
async def google_login(request: Request):
    """
    Endpoint to initiate Google OAuth2 login
    Args:
        request (Request): FastAPI request object
    Returns:
        Redirect to Google OAuth2 login page
    """

    return await oauth.google.authorize_redirect(
        request, settings.GOOGLE_REDIRECT_URL
    )


@auth.get(
    path="/google/callback",
    response_model=schemas.AuthResponse,
    summary="Google OAuth2 Callback",
    description="This endpoint handles the callback from Google after OAuth2 login",
    tags=["Authentication"],
)
async def google_callback(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint to handle Google OAuth2 callback

    Args:
        request (Request): FastAPI request object
        db (Annotated[Session, Depends): Database session

    Returns:
        AuthResponse: Response containing access and refresh tokens
    """

    try:
        token: OAuth2Token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google OAuth error: {e.error}",
        )

    service = UserService(db=db)

    user = service.google_auth(token=token)

    # Create access and refresh tokens
    access_token = jwt_helpers.create_jwt_token("access", user.id)
    refresh_token = jwt_helpers.create_jwt_token("refresh", user.id)

    response_data = schemas.AuthResponseData(id=user.id, username=user.username)

    return schemas.AuthResponse(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        access_token=access_token,
        refresh_token=refresh_token,
        data=response_data,
    )


@auth.get("/user")
def get_user(current_user: Annotated[User, Depends(get_current_user)]):
    user_schema = schemas.AuthResponseData(
        id=current_user.id, username=current_user.username
    )

    return schemas.UserResponse(
        status_code=status.HTTP_200_OK,
        message="User Details Retrieved",
        data=user_schema,
    )
