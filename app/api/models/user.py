"""User data model"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.base.model import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "users"

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)

    # Relationship
    decks = relationship("Deck", back_populates="user", cascade="all, delete-orphan")

    def __str__(self):
        return "User: {}".format(self.username)
