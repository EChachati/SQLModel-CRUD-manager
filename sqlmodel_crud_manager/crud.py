from dataclasses import dataclass
from typing import TypeVar

from fastapi import HTTPException, status
from sqlalchemy.engine.base import Engine
from sqlmodel import Session, SQLModel, select
from sqlmodel.sql.expression import Select

ModelType = TypeVar("ModelType", bound=SQLModel)
ModelCreateType = TypeVar("ModelCreateType", bound=SQLModel)
QueryLike = TypeVar("QueryLike", bound=Select)


@dataclass
class CRUDManager:
    model: ModelType

    def __init__(self, model: ModelType, engine: Engine):
        """
        The function initializes an object with a model and a database session.

        Arguments:

        * `model`: The model object represents a specific model or entity in the
        application. It could be a database model, a machine learning model, or
        any other type of model
        """
        self.model = model
        self.db = Session(engine)

    def get(self, pk: int) -> ModelType:
        """
        The function retrieves a model object from the database based on its
        primary key and raises an exception if the object is not found.

        Arguments:

        * `pk`: The parameter `pk` stands for "primary key" and it is of type
        `int`. It is used to identify a specific object in the database based
        on its primary key value.

        Returns:

        The `get` method is returning an instance of the `ModelType` class.
        """
        query = select(self.model).where(self.model.id == pk)
        obj = self.db.exec(query).one_or_none()
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model} with ID: {pk} Not Found",
            )
        return obj

    def list(self, query: QueryLike = None) -> list[ModelType]:
        """
        The function returns a list of all the records in the database that
        match the given query.

        Arguments:

        * `query`: The `query` parameter is an optional argument of type
        `QueryLike`. It represents a query that will be executed on the
        database. If no query is provided, the function will use a default
        query that selects all records from the `ModelType` table.

        Returns:

        a list of objects of type `ModelType`.
        """
        if query is None:
            query = select(self.model)
        return self.db.exec(query).all()

    def create(self, object: ModelCreateType) -> ModelType:
        """
        The function creates a new object in the database and returns it.

        Arguments:

        * `object`: The "object" parameter is of type ModelCreateType, which is
        the type of the object that you want to create.

        Returns:

        The `create` method is returning an object of type `ModelType`.
        """
        with self.db:
            obj = self.model.model_validate(object)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
        return obj

    def update(self, input_object: ModelType) -> ModelType:
        """
        The function updates a database object with the values from an input
        object and returns the updated object.

        Arguments:

        * `input_object`: The input_object parameter is an instance of the
        ModelType class. It represents the object that contains the updated
        values for the fields of the database object.

        Returns:

        The `update` method is returning the `db_object` after it has been
        updated in the database.
        """
        db_object = self.get(input_object.id)
        for field in input_object.model_fields:
            setattr(db_object, field, getattr(input_object, field))
        self.db.add(db_object)
        self.db.commit()
        self.db.refresh(db_object)
        return db_object

    def delete(self, pk: int) -> ModelType:
        """
        The function deletes a database object with a given primary key and
        returns the deleted object.

        Arguments:

        * `pk`: The "pk" parameter stands for "primary key" and it is used to
        identify a specific object in the database. In this context, it is an
        integer value that represents the primary key of the object that needs
        to be deleted.

        Returns:

        The `delete` method is returning the `db_object` that was deleted from
        the database.
        """
        db_object = self.get(pk)
        self.db.delete(db_object)
        self.db.commit()
        return db_object
