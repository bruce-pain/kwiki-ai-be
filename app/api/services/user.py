from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token

from app.utils import password_utils
from app.api.v1.auth import schemas
from app.api.models.user import User
from app.api.repositories.user import UserRepository
from app.utils.logger import logger
from app.utils.google_oauth import oauth

class UserService:
    """
    User service class for handling user-related operations.
    This class provides methods for user registration and authentication.
    """

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register(self, schema: schemas.RegisterRequest) -> User:
        """Creates a new user
        Args:
            schema (schemas.RegisterRequest): Registration schema
        Returns:
            User: User object for the newly created user
        """
        # check if user with email already exists
        if self.repository.get_by_username(schema.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists!",
            )

        # Hash password
        schema.password = password_utils.hash_password(password=schema.password)

        user = User(**schema.model_dump())

        logger.info(f"Creating user with username: {user.username}")
        return self.repository.create(user)
    
    def google_auth(self, token: OAuth2Token) -> User:
        """Authenticates a user using Google OAuth
        Args:
            token (OAuth2Token): OAuth2 token from Google
        Returns:
            User: Authenticated user
        """
        # Get user info from the token
        try:
            user_info = oauth.google.parse_id_token(token)
        except OAuthError as e:
            logger.error(f"OAuth error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        # Check if user with the email already exists
        user = self.repository.get_by_username(user_info["email"])

        if not user:
            # Create a new user if not exists
            user = User(username=user_info["email"])
            self.repository.create(user)

        logger.info(f"User authenticated with email by Google: {user.username}")
        return user
    
    def authenticate(self, schema: schemas.LoginRequest) -> User:
        """Authenticates a registered user
        Args:
            schema (schemas.LoginRequest): Login Request schema
        Returns:
            User: Authenticated user
        """
        # check if user with the username exists
        user = self.repository.get_by_username(schema.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username",
            )

        if not password_utils.verify_password(schema.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password",
            )

        logger.info(f"User authenticated with username: {user.username}")
        return user