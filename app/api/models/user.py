"""User data model"""

from sqlalchemy import Column, String
from app.core.base.model import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "users"

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)

    def __str__(self):
        return "User: {}".format(self.username)
