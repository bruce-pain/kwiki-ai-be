from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session

from app.core.base.model import BaseTableModel

Model = TypeVar("T", bound=BaseTableModel)


class BaseRepository(Generic[Model]):
    """
    Base repository class for CRUD operations.
    This class provides a generic interface for performing CRUD operations on SQLAlchemy models.
    It is designed to be inherited by specific repository classes for different models.
    Attributes:
        model (Type[Model]): The SQLAlchemy model class.
        db (Session): The SQLAlchemy session.
    """

    def __init__(self, model: Type[Model], db: Session):
        self.model = model
        self.db = db

    def create(self, obj: Model) -> Model:
        """Create a new object of the model.
        Args:
            obj (Model): The object to be created.
        Returns:
            Model: The created object.
        """

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, id: str) -> Optional[Model]:
        """Get an object of the model by id.
        Args:
            id (str): The id of the object.
        Returns:
            Optional[Model]: The object if found, None otherwise.
        """

        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[Model]:
        """Get all objects of the model.

        This method retrieves all records from the database for the current model.

        Returns:
            List[Model]: A list containing all objects of the model in the database.
        """

        return self.db.query(self.model).all()

    def update(self, obj: Model) -> Model:
        """Update an existing object of the model.

        This method updates an existing record in the database with the provided object's data.
        It first checks if the object exists, then updates all attributes based on the provided object.

        Args:
            obj (Model): The object containing updated data.

        Returns:
            Model: The updated object if successful, None if the object wasn't found.
        """

        existing_obj = self.get(obj.id)
        if existing_obj:
            for key, value in obj.__dict__.items():
                setattr(existing_obj, key, value)
            self.db.commit()
            self.db.refresh(existing_obj)
            return existing_obj
        return None

    def delete(self, id: str) -> bool:
        """Delete an object of the model by id.

        This method removes a record from the database based on the provided id.

        Args:
            id (str): The id of the object to delete.

        Returns:
            bool: True if the object was successfully deleted, False if the object wasn't found.
        """

        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
