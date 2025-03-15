from sqlalchemy.orm import Session
from app.api.repositories.flashcard import FlashCardRepository
from app.api.models.flashcard import Flashcard

class FlashCardService:
    """
    Flashcard service class for handling flashcard-related operations.
    This class provides methods for flashcard management, including creating, updating, deleting, and retrieving flashcards.
    """

    def __init__(self, db: Session):
        self.repository = FlashCardRepository(db)

    def create_flashcard(self, question: str, answer: str, deck_id: str) -> Flashcard:
        """
        Create a new flashcard.
        Args:
            question (str): The question for the flashcard.
            answer (str): The answer for the flashcard.
            deck_id (str): The ID of the deck to which the flashcard belongs.
        Returns:
            Flashcard: The created flashcard object.
        """
        return self.repository.create(
            question=question, answer=answer, deck_id=deck_id
        )