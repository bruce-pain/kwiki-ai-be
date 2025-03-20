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

class DeckResponseModel(DeckModel):
    id: str
    user_id: str

# Request schemas
class CreateDeckRequest(BaseModel):
    topic: str

# Response schemas
class CreateDeckResponse(BaseResponseModel):
    data: DeckResponseModel

class GetListDeckResponse(BaseResponseModel):
    data: List[DeckResponseModel]