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

    def get_all_user_decks(self, user_id: str) -> list[Deck]:
        """
        Get all decks for a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list[Deck]: A list of Deck objects associated with the user.
        """
        return self.db.query(self.model).filter(self.model.user_id == user_id).all()
    
    def get_user_deck_by_id(self, deck_id: str, user_id: str) -> Deck:
        """
        Get a specific deck belonging to a user by deck ID.
        Args:
            deck_id (str): The ID of the deck to retrieve
            user_id (str): The ID identifier of the user who owns the deck
        Returns:
            Deck: The deck object if found
        """
        
        return self.db.query(self.model).filter(
            self.model.id == deck_id,
            self.model.user_id == user_id
        ).first()