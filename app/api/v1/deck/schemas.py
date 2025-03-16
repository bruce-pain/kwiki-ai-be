from typing import List

from pydantic import BaseModel

class Flashcard(BaseModel):
    question: str
    answer: str
    explanation: str


class DeckModel(BaseModel):
    title: str
    description: str
    cards: List[Flashcard]