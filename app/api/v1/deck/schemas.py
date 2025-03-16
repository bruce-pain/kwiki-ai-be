from typing import List

from pydantic import BaseModel

class Flashcard(BaseModel):
    question: str
    answer: str
    explanation: str


class Deck(BaseModel):
    title: str
    description: str
    cards: List[Flashcard]