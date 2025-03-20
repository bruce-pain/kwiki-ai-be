from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.database import get_db
from app.core.dependencies.security import get_current_user

from app.api.v1.deck.schemas import (
    # DeckModel,
    CreateDeckRequest,
    CreateDeckResponse,
    GetListDeckResponse,
)

# from app.api.models.deck import Deck
from app.api.models.user import User

from app.api.services.deck import DeckService
from app.api.services.llm import LLMService

deck_router = APIRouter(prefix="/decks", tags=["Deck"])


@deck_router.post(
    path="/generate",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateDeckResponse,
    summary="Generate a new deck",
    description="This endpoint generates a new deck based on the provided topic and returns the generated deck",
    tags=["Deck"],
)
def generate_deck(
    schema: CreateDeckRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> CreateDeckResponse:
    """Endpoint for generating a new deck based on a topic

    Args:
        schema (CreateDeckRequest): Request schema containing the topic
        db (Annotated[Session, Depends]): Database session
        current_user (Annotated[User, Depends]): Current authenticated user

    Returns:
        CreateDeckResponse: Response schema containing the generated deck
    """
    # Generate deck using LLM
    llm_service = LLMService()
    try:
        generated_deck = llm_service.generate_deck_from_topic(topic=schema.topic)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating deck: {str(e)}",
        )

    # Save deck to database
    deck_service = DeckService(db=db)
    deck = deck_service.save_deck(deck_model=generated_deck, user_id=current_user.id)

    return CreateDeckResponse(
        status_code=status.HTTP_201_CREATED,
        message="Deck generated successfully",
        data=deck.to_dict(),
    )


@deck_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=GetListDeckResponse,
    summary="Get list of decks",
    description="This endpoint retrieves a list of all decks",
    tags=["Deck"],
)
def get_list_deck(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Endpoint for retrieving a list of all decks
    Args:
        db (Annotated[Session, Depends]): Database session
        current_user (Annotated[User, Depends]): Current authenticated user

    Returns:
        GetListDeckResponse: Response schema containing the list of decks
    """

    deck_service = DeckService(db=db)
    decks = deck_service.get_user_decks(user_id=current_user.id)

    return GetListDeckResponse(
        status_code=status.HTTP_200_OK,
        message="Decks retrieved successfully",
        data=[deck.to_dict() for deck in decks],
    )