from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.repositories.deck import DeckRepository
from app.api.services.flashcard import FlashCardService
from app.api.models.deck import Deck
from app.api.v1.deck.schemas import DeckModel as DeckModel
from app.utils.logger import logger

class DeckService:
    """
    Deck service class for handling deck-related operations.
    This class provides methods for deck management, including creating, updating, deleting, and retrieving decks.
    """

    def __init__(self, db: Session):
        """
        Initialize the DeckService with a database session.

        Args:
            db (Session): The SQLAlchemy session.
        """
        self.repository = DeckRepository(db)
        self.flashcard_service = FlashCardService(db)

    def save_deck(self, deck_model: DeckModel, user_id: str) -> Deck:
        """
        Save a new deck to the database.
        This method creates a new deck and its associated flashcards if provided.

        Args:
            deck_model (DeckModel): The deck model containing the deck data.
            user_id (str): The ID of the user creating the deck.

        Returns:
            Deck: The created deck object.
        """
        new_deck = Deck(
            name=deck_model.name,
            description=deck_model.description,
            user_id=user_id,
        )
        new_deck = self.repository.create(new_deck)

        # Create flashcards if provided
        if deck_model.cards:
            for card in deck_model.cards:
                self.flashcard_service.create_flashcard(
                    question=card.question,
                    answer=card.answer,
                    explanation=card.explanation,
                    deck_id=new_deck.id,
                )

        logger.info(f"Deck created with ID: {new_deck.id} and title: {new_deck.name}")
        return new_deck

    def get_deck(self, deck_id: str) -> Deck:
        """
        Get a deck by its ID.

        Args:
            deck_id (str): The ID of the deck.

        Returns:
            Optional[Deck]: The deck object if found, None otherwise.
        """
        deck = self.repository.get(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deck with ID {deck_id} not found",
            )

        logger.info(f"Fetching deck with ID: {deck_id}")
        return deck

    def get_user_decks(self, user_id: str) -> List[Deck]:
        """
        Get all decks for a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            List[Deck]: A list of decks belonging to the user.
        """
        decks = self.repository.get_user_decks(user_id)

        logger.info(f"Fetching decks for user with ID: {user_id}")
        return decks

    def update_deck(self, deck_id: str, name: str, description: str) -> Optional[Deck]:
        """
        Update an existing deck.

        Args:
            deck_id (str): The ID of the deck to update.
            name (str): The new name of the deck.
            description (str): The new description of the deck.

        Returns:
            Optional[Deck]: The updated deck object if found, None otherwise.
        """
        deck = self.repository.get(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deck with ID {deck_id} not found",
            )

        deck.name = name
        deck.description = description

        logger.info(f"Updating deck with ID: {deck_id} to name: {name} and description: {description}")
        return self.repository.update(deck)

    def delete_deck(self, deck_id: str) -> bool:
        """
        Delete a deck by its ID.

        Args:
            deck_id (str): The ID of the deck to delete.

        Returns:
            bool: True if the deck was deleted, False otherwise.
        """
        deck = self.repository.get(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deck with ID {deck_id} not found",
            )

        self.repository.delete(deck)

        logger.info(f"Deck with ID: {deck_id} deleted successfully")
        return True
