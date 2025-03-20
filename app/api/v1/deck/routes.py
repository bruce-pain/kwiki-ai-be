from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.database import get_db
from app.core.dependencies.security import get_current_user

from app.api.v1.deck.schemas import (
    # DeckModel,
    CreateDeckRequest,
    CreateDeckResponse,
    GetDeckResponse,
    GetListDeckResponse,
    UpdateDeckRequest,
    UpdateDeckResponse,
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

@deck_router.get(
    path="/{deck_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetDeckResponse,
    summary="Get deck by ID",
    description="This endpoint retrieves a deck by its ID",
    tags=["Deck"],
)
def get_deck(
    deck_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> GetDeckResponse:
    """
    Endpoint for retrieving a deck by its ID

    Args:
        deck_id (str): ID of the deck to retrieve
        db (Annotated[Session, Depends]): Database session
        current_user (Annotated[User, Depends]): Current authenticated user

    Returns:
        GetDeckResponse: Response schema containing the retrieved deck
    """
    deck_service = DeckService(db=db)
    deck = deck_service.get_deck(deck_id=deck_id)

    return GetDeckResponse(
        status_code=status.HTTP_200_OK,
        message="Deck retrieved successfully",
        data=deck.to_dict(),
    )

@deck_router.patch(
    path="/{deck_id}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateDeckResponse,
    summary="Update deck by ID",
    description="This endpoint updates a deck by its ID",
    tags=["Deck"],
)
def update_deck(
    deck_id: str,
    schema: UpdateDeckRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UpdateDeckResponse:
    """
    Endpoint for updating a deck by its ID

    Args:
        deck_id (str): ID of the deck to update
        schema (UpdateDeckRequest): Request schema containing the updated deck data
        db (Annotated[Session, Depends]): Database session
        current_user (Annotated[User, Depends]): Current authenticated user

    Returns:
        UpdateDeckResponse: Response schema containing the updated deck
    """
    deck_service = DeckService(db=db)
    deck = deck_service.update_deck(deck_id=deck_id, schema=schema)

    return UpdateDeckResponse(
        status_code=status.HTTP_200_OK,
        message="Deck updated successfully",
        data=deck.to_dict(),
    )

@deck_router.delete(
    path="/{deck_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete deck by ID",
    description="This endpoint deletes a deck by its ID",
    tags=["Deck"],
)
def delete_deck(
    deck_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Endpoint for deleting a deck by its ID

    Args:
        deck_id (str): ID of the deck to delete
        db (Annotated[Session, Depends]): Database session
        current_user (Annotated[User, Depends]): Current authenticated user

    Returns:
        None
    """
    deck_service = DeckService(db=db)
    deck_service.delete_deck(deck_id=deck_id)

    return None