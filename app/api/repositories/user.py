from sqlalchemy.orm import Session
from app.core.base.repository import BaseRepository
from app.api.models.user import User


class UserRepository(BaseRepository[User]):
    """
    User repository class for CRUD operations on User model.
    This class inherits from BaseRepository and provides specific methods for User model.
    Attributes:
        model (Type[User]): The SQLAlchemy User model class.
        db (Session): The SQLAlchemy session.
    """

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_username(self, username: str) -> User:
        """Get a user by username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The user object if found, None otherwise.
        """
        return self.db.query(self.model).filter(self.model.username == username).first()
