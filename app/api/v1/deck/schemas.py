from typing import List

from pydantic import BaseModel

from app.core.base.schema import BaseResponseModel


class Flashcard(BaseModel):
    question: str
    answer: str
    explanation: str


class DeckModel(BaseModel):
    name: str
    description: str
    cards: List[Flashcard]


class BaseDeckModel(DeckModel):
    id: str
    user_id: str


class ListDeckModel(BaseModel):
    name: str
    description: str
    id: str
    user_id: str


# Request schemas
class CreateDeckRequest(BaseModel):
    topic: str


class UpdateDeckRequest(BaseModel):
    name: str | None = None
    description: str | None = None


# Response schemas


class BaseDeckResponse(BaseResponseModel):
    data: BaseDeckModel


class CreateDeckResponse(BaseDeckResponse):
    pass


class GetDeckResponse(BaseDeckResponse):
    pass


class UpdateDeckResponse(BaseDeckResponse):
    pass


class GetListDeckResponse(BaseResponseModel):
    data: List[ListDeckModel]
