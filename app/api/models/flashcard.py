"""Flashcard data model"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base.model import BaseTableModel


class Flashcard(BaseTableModel):
    __tablename__ = "flashcards"

    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    explanation = Column(String, nullable=True)
    deck_id = Column(String, ForeignKey("decks.id"), nullable=False)

    # Relationship
    deck = relationship("Deck", back_populates="cards")

    def __str__(self):
        return f"Flashcard: {self.question[:30]}..."
    
    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "explanation": self.explanation,
            "deck_id": self.deck_id
        }