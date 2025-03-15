"""Deck data model"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base.model import BaseTableModel


class Deck(BaseTableModel):
    __tablename__ = "decks"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Relationship
    cards = relationship("Flashcard", back_populates="deck", cascade="all, delete-orphan")
    user = relationship("User", back_populates="decks")

    def __str__(self):
        return f"Deck: {self.name}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id,
            "cards": [card.to_dict() for card in self.cards]
        }