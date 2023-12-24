# SQLModel CRUD Manager

[![Tests](https://github.com/EChachati/SQLModel-CRUD-manager/actions/workflows/testing.yml/badge.svg?branch=master)](https://github.com/EChachati/SQLModel-CRUD-manager/actions/workflows/testing.yml)
[![Ruff](https://github.com/EChachati/SQLModel-CRUD-manager/actions/workflows/linter.yml/badge.svg)](https://github.com/EChachati/SQLModel-CRUD-manager/actions/workflows/linter.yml)
[![pypi](https://img.shields.io/pypi/v/SQLModel-CRUD-manager.svg)](https://pypi.python.org/pypi/SQLModel-CRUD-manager)
[![versions](https://img.shields.io/pypi/pyversions/SQLModel-CRUD-manager.svg)](https://github.com/EChachati/SQLModel-CRUD-manager)
[![license](https://img.shields.io/github/license/EChachati/SQLModel-CRUD-manager.svg)](https://github.com/EChachati/SQLModel-CRUD-manager/blob/master/LICENSE)

## Introduction

The SQLModel CRUD Manager is a Python library that facilitates common Create, Read, Update, and Delete (CRUD) operations on SQLModel entities within a FastAPI application. This library simplifies database interactions and provides an easy-to-use interface for managing SQLModel entities.

## Installation

You can install the SQLModel CRUD Manager using pip:

```bash
pip install SQLModel-CRUD-manager
```

## Usage

### Example

Here's a simple example demonstrating how to use the SQLModel CRUD Manager within a FastAPI application:

```python
from fastapi import APIRouter, status
from sqlmodel_crud_manager import CRUDManager
from core.sql.database import engine as db_engine
from core.sql.models import YourModel, YourModelCreate

router = APIRouter()

# Initializing CRUD Manager with YourModel model and database engine
crud = CRUDManager(YourModel, db_engine)

@router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=YourModel)
def get_your_model(pk: int):
    return crud.get(pk)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=YourModel)
def create_your_model(YourModel: YourModelCreate):
    return crud.create(YourModel)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[YourModel])
def list_your_model():
    return crud.list()

@router.put("/", status_code=status.HTTP_200_OK, response_model=YourModel)
def update_your_model(YourModel: YourModel):
    return crud.update(YourModel)

@router.delete("/{pk}")
def delete_your_model(pk: int):
    return crud.delete(pk)
```

## CRUDManager Class

The CRUDManager class provides the following methods:

- `get(pk: int) -> ModelType`: Retrieve an object based on its primary key.
- `get_by_ids(ids:list[int]) -> list[ModelType]`:  Get a list of records matching the keys sent
- `list(query: QueryLike = None) -> list[ModelType]`: Get a list of records matching the query.
- `create(object: ModelCreateType) -> ModelType`: Create a new object in the database.
- `update(input_object: ModelType) -> ModelType`: Update an object in the database.
- `delete(pk: int) -> ModelType`: Delete an object based on its primary key.

### Initialization

To use the CRUDManager class, initialize it with a model and a database engine:

```python
from sqlmodel_crud_manager import CRUDManager
from sqlalchemy import create_engine
from sqlmodel import SQLModel

engine = create_engine("sqlite:///example.db")

# Replace `YourModel` and `YourModelCreate` with your actual model classes
class YourModelCreate(SQLModel):
    name: str
    phone: PhoneNumber


class YourModel(YourModelCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)

crud = CRUDManager(YourModel, engine)
```

## Requirements

- sqlalchemy
- sqlmodel
- fastapi

## License

This library is licensed under the MIT License.

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

Feel free to expand on this README by adding details about specific methods, advanced usage, or any additional configurations. It's important to provide clear examples and instructions to help users quickly understand and utilize your library.
