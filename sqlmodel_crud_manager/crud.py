from dataclasses import dataclass
from typing import List, TypeVar

from fastapi import HTTPException, status
from sqlalchemy.engine.base import Engine
from sqlmodel import Session, SQLModel, select
from sqlmodel.sql.expression import Select

from sqlmodel_crud_manager.decorator import for_all_methods, raise_as_http_exception

ModelType = TypeVar("ModelType", bound=SQLModel)
ModelCreateType = TypeVar("ModelCreateType", bound=SQLModel)
QueryLike = TypeVar("QueryLike", bound=Select)


@dataclass
@for_all_methods(raise_as_http_exception)
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

    def __validate_field_exists(self, field: str) -> None:
        if field not in self.model.model_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self.model} does not have a {field} field",
            )

    def __raise_not_found(self, detail: str) -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    def get(self, pk: int, db: Session = None) -> ModelType:
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
        self.db = db or self.db
        query = select(self.model).where(self.model.id == pk)
        return self.db.exec(query).one_or_none()

    def get_or_404(self, pk: int, db: Session = None) -> ModelType:
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
        if obj := self.get(pk, db=db):
            print(obj)
            return obj
        self.__raise_not_found(f"{self.model.__name__} with id {pk} not found")

    def get_by_ids(self, ids: list[int], db: Session = None) -> list[ModelType]:
        """
        The function retrieves a list of model objects from the database based
        on their primary keys.

        Arguments:

        * `ids`: The parameter `ids` is a list of integers. It is used to
        identify a list of objects in the database based on their primary key
        values.

        Returns:

        The `get_by_ids` method is returning a list of objects of type
        `ModelType`.
        """
        self.db = db or self.db
        query = select(self.model).where(self.model.id.in_(ids))
        return self.db.exec(query).all()

    def get_by_field(
        self,
        field: str,
        value: str,
        allows_multiple: bool = False,
        db: Session = None,
    ) -> ModelType:
        """
        The function retrieves a model object from the database based on a
        field and a value.

        Arguments:

        * `field`: The parameter `field` is a string that represents the name
        of a field in the database table.

        * `value`: The parameter `value` is a string that represents the value
        of a field in the database table.

        Returns:

        The `get_by_field` method is returning an object of type `ModelType`.
        """
        self.db = db or self.db
        self.__validate_field_exists(field)

        query = select(self.model).where(getattr(self.model, field) == value)
        if allows_multiple:
            return self.db.exec(query).all()
        return self.db.exec(query).one_or_none()

    def get_by_fields(
        self,
        fields: dict[str, str],
        *,
        allows_multiple: bool = False,
        db: Session = None,
    ) -> list[ModelType] | ModelType:
        """
        The function retrieves a list of model objects from the database based
        on a dictionary of fields and values.

        Arguments:

        * `fields`: The parameter `fields` is a dictionary of strings that
        represents the name of a field in the database table and the value of
        that field.

        Returns:

        The `get_by_fields` method is returning a list of objects of type
        `ModelType`.
        """
        self.db = db or self.db
        query = select(self.model)
        for field, value in fields.items():
            self.__validate_field_exists(field)
            query = query.where(getattr(self.model, field) == value)
        if allows_multiple:
            return self.db.exec(query).all()
        return self.db.exec(query).one_or_none()

    def get_or_create(
        self,
        object: ModelCreateType,
        search_field: str = "id",
        db: Session = None,
    ) -> ModelType:
        """
        The function `get_or_create` checks if an object exists in the database based
        on a specified search field, and either returns the object if it exists
        or creates a new object if it doesn't.

        Arguments:

        * `object`: The `object` parameter is the object that you want to get or
        create in the database. It should be of type `ModelCreateType`, which is the
        type of the object that you want to create.
        * `search_field`: The `search_field` parameter is a string that specifies the
        field to search for when checking if an object already exists in the database.
        By default, it is set to "id", meaning it will search for an object with the
        same id as the one being passed in.
        * `db`: The `db` parameter is an optional parameter of type `Session`.
        It represents the database session that will be used for the database operations
        If no session is provided, it will use the default session.

        Returns:

        The function `get_or_create` returns an instance of `ModelType`.
        """
        self.db = db or self.db
        self.__validate_field_exists(search_field)

        if obj := self.get_by_field(
            search_field,
            getattr(object, search_field),
            db=db,
        ):
            return obj
        else:
            return self.create(object, db=db)

    def list(self, query: QueryLike = None, db: Session = None) -> list[ModelType]:
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
        self.db = db or self.db
        query = query or select(self.model)
        return self.db.exec(query).all()

    def create(self, object: ModelCreateType, db: Session = None) -> ModelType:
        """
        The function creates a new object in the database and returns it.

        Arguments:

        * `object`: The "object" parameter is of type ModelCreateType, which is
        the type of the object that you want to create.

        Returns:

        The `create` method is returning an object of type `ModelType`.
        """
        self.db = db or self.db
        obj = self.model.model_validate(object)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def create_or_update(
        self,
        object: ModelCreateType,
        search_field: str = "id",
        db: Session = None,
    ) -> ModelType:
        """
        The function `create_or_update` checks if an object exists in the database based
        on a specified search field, and either updates the object if it exists
        or creates a new object if it doesn't.

        Arguments:

        * `object`: The `object` parameter is the object that you want to create or
        update in the database. It should be of type `ModelCreateType`, which is the
        type of the object that you want to create.
        * `search_field`: The `search_field` parameter is a string that specifies the
        field to search for when checking if an object already exists in the database.
        By default, it is set to "id", meaning it will search for an object with the
        same id as the one being passed in.
        * `db`: The `db` parameter is an optional parameter of type `Session`.
        It represents the database session that will be used for the database operations
        If no session is provided, it will use the default session.

        Returns:

        The function `create_or_update` returns an instance of `ModelType`.
        """
        self.db = db or self.db
        self.__validate_field_exists(search_field)

        if obj := self.get_by_field(
            search_field,
            getattr(object, search_field),
            db=db,
        ):
            new_object = self.model.model_validate(object)
            new_object.id = obj.id
            return self.update(new_object, db=db)
        else:
            return self.create(object, db=db)

    def create_or_update_by_fields(
        self,
        object: ModelCreateType,
        fields: List[str],
        db: Session = None,
    ) -> ModelType:
        """
        The function `create_or_update_by_fields` creates or updates a model object
        based on specified fields.

        Arguments:

        * `object`: The `object` parameter is the object that you want to create or
        update in the database. It should be of type `ModelCreateType`, which is the
        type of the object that can be created in the database.
        * `fields`: The `fields` parameter is a list of strings that represents
        the fields (attributes) of the object that are used to check for existing
        records in the database. These fields are used to query the database and
        determine if a record with the same values already exists.
        * `db`: The `db` parameter is an optional argument of type `Session`. It
        represents the database session that will be used for database operations.
        If no session is provided, the method will use the default session stored in
        the `self.db` attribute.

        Returns:

        The function `create_or_update_by_fields` returns a `ModelType` object.
        """
        self.db = db or self.db
        for field in fields:
            self.__validate_field_exists(field)

        if obj := self.get_by_fields(
            {field: getattr(object, field) for field in fields},
            db=db,
        ):
            new_object = self.model.model_validate(object)
            new_object.id = obj.id
            return self.update(new_object, db=db)
        else:
            return self.create(object, db=db)

    def update(self, input_object: ModelType, db: Session = None) -> ModelType:
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
        self.db = db or self.db
        db_object = self.get(input_object.id)
        for field in input_object.model_fields:
            setattr(db_object, field, getattr(input_object, field))
        self.db.add(db_object)
        self.db.commit()
        self.db.refresh(db_object)
        return db_object

    def delete(self, pk: int, db: Session = None) -> ModelType:
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
        self.db = db or self.db
        db_object = self.get_or_404(pk)
        self.db.delete(db_object)
        self.db.commit()
        return db_object
