from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.utils import password_utils
from app.core import response_messages
from app.api.v1.auth import schemas
from app.api.models.user import User


def register(db: Session, schema: schemas.RegisterRequest) -> User:
    """Creates a new user

    Args:
        db (Session): Database Session
        schema (schemas.RegisterRequest): Registration schema

    Returns:
        User: User object for the newly created user
    """

    # check if user with email already exists
    if db.query(User).filter(User.username == schema.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists!",
        )

    # Hash password
    schema.password = password_utils.hash_password(password=schema.password)

    user = User(**schema.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate(db: Session, schema: schemas.LoginRequest) -> User:
    """Authenticates a registered user

    Args:
        db (Session): Database Session
        schema (schemas.LoginRequest): Login Request schema

    Returns:
        User: Authenticated user
    """

    # check if user with the email exists
    user = db.query(User).filter(User.username == schema.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response_messages.INVALID_EMAIL,
        )

    if not password_utils.verify_password(schema.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response_messages.INVALID_PASSWORD,
        )

    return user
