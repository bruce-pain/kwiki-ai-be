from sqlalchemy.orm import Session
from app.core.base.repository import BaseRepository
from app.api.models.deck import Deck


class DeckRepository(BaseRepository[Deck]):
    """
    Deck repository class for CRUD operations on Deck model.
    This class provides a specific interface for performing CRUD operations on the Deck model.
    It inherits from the BaseRepository class.
    Attributes:
        db (Session): The SQLAlchemy session.
    """

    def __init__(self, db: Session):
        super().__init__(Deck, db)

    def get_user_decks(self, user_id: str) -> list[Deck]:
        """
        Get all decks for a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list[Deck]: A list of Deck objects associated with the user.
        """
        return self.db.query(self.model).filter(self.model.user_id == user_id).all()
