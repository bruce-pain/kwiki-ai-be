from sqlalchemy.orm import Session
from app.core.base.repository import BaseRepository
from api.models.flashcard import Flashcard

class FlashCardRepository(BaseRepository[Flashcard]):
    """
    Flashcard repository class for CRUD operations on Flashcard model.
    This class provides a specific interface for performing CRUD operations on the Flashcard model.
    It inherits from the BaseRepository class.
    Attributes:
        db (Session): The SQLAlchemy session.
    """

    def __init__(self, db: Session):
        super().__init__(Flashcard, db)