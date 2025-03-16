from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.api.repositories.flashcard import FlashCardRepository
from app.api.repositories.deck import DeckRepository
from app.api.models.flashcard import Flashcard
from app.utils.logger import logger


class FlashCardService:
    """
    Flashcard service class for handling flashcard-related operations.
    This class provides methods for flashcard management, including creating, updating, deleting, and retrieving flashcards.
    """

    def __init__(self, db: Session):
        self.repository = FlashCardRepository(db)
        self.deck_repository = DeckRepository(db)

    def create_flashcard(self, question: str, answer: str, explanation: str, deck_id: str) -> Flashcard:
        """
        Create a new flashcard.
        Args:
            question (str): The question for the flashcard.
            answer (str): The answer for the flashcard.
            deck_id (str): The ID of the deck to which the flashcard belongs.
        Returns:
            Flashcard: The created flashcard object.
        """

        # Validate deck ID
        deck = self.deck_repository.get(deck_id)
        if not deck:
            logger.error(f"Deck with ID {deck_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deck with ID {deck_id} not found.",
            )
        
        new_flashcard = Flashcard(
            question=question,
            answer=answer,
            explanation=explanation,
            deck_id=deck.id,
        )

        new_flashcard = self.repository.create(new_flashcard)

        logger.info(
            f"Creating flashcard with ID: {new_flashcard.id} and question: {new_flashcard.question} for deck ID: {deck.id}"
        )
        return new_flashcard
