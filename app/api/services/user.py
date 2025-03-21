from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.utils import password_utils
from app.api.v1.auth import schemas
from app.api.models.user import User
from app.api.repositories.user import UserRepository
from app.utils.logger import logger


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