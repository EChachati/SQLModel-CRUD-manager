import pytest
from fastapi import HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

from sqlmodel_crud_manager.crud import CRUDManager


class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: int | None = None
    is_alive: bool = True


class Hero(HeroCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)


SECRET_NAME = "Dive Wilson"
HERO_NAME = "Deadpond"


engine = create_engine("sqlite:///tests/testing.db")
SQLModel.metadata.create_all(engine)
crud = CRUDManager(Hero, engine)


@pytest.fixture(name="last_id")
def get_last_id_fixture():
    return Session(engine).exec(select(Hero).order_by(Hero.id.desc())).first().id


def test_create():
    hero = HeroCreate(name=HERO_NAME, secret_name=SECRET_NAME)
    hero = crud.create(hero)
    assert hero.id is not None
    assert hero.name == HERO_NAME
    assert hero.secret_name == SECRET_NAME
    assert hero.age is None
    assert hero.is_alive is True


def test_get(last_id):
    hero = crud.get(last_id)
    assert hero.id == last_id
    assert hero.name == HERO_NAME
    assert hero.secret_name == SECRET_NAME
    assert hero.age is None
    assert hero.is_alive is True


def test_get_or_404(last_id):
    hero = crud.get_or_404(last_id)
    assert hero.id == last_id
    assert hero.name == HERO_NAME
    assert hero.secret_name == SECRET_NAME
    assert hero.age is None
    assert hero.is_alive is True

    with pytest.raises(HTTPException):
        crud.get_or_404(last_id + 1)


def test_get_by_ids(last_id):
    heroes = crud.get_by_ids([last_id])
    assert len(heroes) == 1
    assert heroes[0].id == last_id
    assert heroes[0].name == HERO_NAME
    assert heroes[0].secret_name == SECRET_NAME
    assert heroes[0].age is None
    assert heroes[0].is_alive is True


def test_get_by_field(last_id):
    heroes = crud.get_by_field("name", HERO_NAME)
    assert heroes.id == last_id
    assert heroes.name == HERO_NAME
    assert heroes.secret_name == SECRET_NAME
    assert heroes.age is None
    assert heroes.is_alive is True

    heroes_list = crud.get_by_field("name", HERO_NAME, allows_multiple=True)
    assert heroes_list[0].id == heroes.id


def test_get_by_field_or_404(last_id):
    heroes = crud.get_by_field_or_404("name", HERO_NAME)
    assert heroes.id == last_id
    assert heroes.name == HERO_NAME
    assert heroes.secret_name == SECRET_NAME
    assert heroes.age is None
    assert heroes.is_alive is True

    with pytest.raises(HTTPException):
        crud.get_by_field_or_404("name", "TotallyNotExistent")


def test_get_by_fields(last_id):
    heroes = crud.get_by_fields({"name": HERO_NAME, "secret_name": SECRET_NAME})
    assert heroes.id == last_id
    assert heroes.name == HERO_NAME
    assert heroes.secret_name == SECRET_NAME
    assert heroes.age is None
    assert heroes.is_alive is True

    heroes_list = crud.get_by_fields(
        {"name": HERO_NAME, "secret_name": SECRET_NAME}, allows_multiple=True
    )
    assert heroes_list[0].id == heroes.id


def test_get_or_create(last_id):
    hero = HeroCreate(name=HERO_NAME, secret_name=SECRET_NAME)
    hero = crud.get_or_create(hero, search_field="name")
    assert hero.id is not None
    assert hero.id == last_id
    assert hero.name == HERO_NAME

    hero = HeroCreate(name="NotExistent", secret_name=SECRET_NAME)
    hero = crud.get_or_create(hero, search_field="name")
    assert hero.id is not None
    assert hero.id != last_id
    assert hero.name == "NotExistent"

    hero = HeroCreate(name="NotExistentV2", secret_name=SECRET_NAME)
    with pytest.raises(HTTPException):
        crud.get_or_create(hero, search_field="id")
    with pytest.raises(HTTPException):
        crud.get_or_create(hero, search_field="NotExistent")


def test_list(last_id):
    heroes = crud.list()
    assert len(heroes) == 2
    assert heroes[-1].id == last_id
    assert heroes[0].name == HERO_NAME
    assert heroes[0].secret_name == SECRET_NAME
    assert heroes[0].age is None
    assert heroes[0].is_alive is True


def test_update(last_id):
    hero = crud.get(last_id)
    hero.name = HERO_NAME
    hero.age = 30
    crud.update(hero)
    hero = crud.get(last_id)
    assert hero.id == last_id
    assert hero.name == HERO_NAME
    assert hero.secret_name == SECRET_NAME
    assert hero.age == 30
    assert hero.is_alive is True


def test_delete(last_id):
    hero = crud.delete(last_id)
    assert hero.id == last_id
    assert hero.name == HERO_NAME
    assert hero.secret_name == SECRET_NAME
    assert hero.age == 30
    assert hero.is_alive is True
    with pytest.raises(HTTPException):
        crud.get_or_404(last_id)


def test_create_or_update(last_id):
    last_hero: Hero = crud.get(last_id)
    hero = HeroCreate(name=last_hero.name, secret_name=last_hero.secret_name)

    hero = crud.create_or_update(hero, search_field="name")
    assert hero.id is not None
    assert hero.id == last_id
    assert hero.name == last_hero.name

    hero = HeroCreate(name="NotExistent_", secret_name=SECRET_NAME)
    hero = crud.create_or_update(hero, search_field="name")
    assert hero.id is not None
    assert hero.id != last_id
    assert hero.name == "NotExistent_"

    hero = HeroCreate(name="NotExistentV2", secret_name=SECRET_NAME)
    with pytest.raises(HTTPException):
        crud.create_or_update(hero, search_field="id")
    with pytest.raises(HTTPException):
        crud.create_or_update(hero, search_field="NotExistent")


def test_create_or_update_by_fields(last_id):
    last_hero: Hero = crud.get(last_id)
    hero = HeroCreate(name=last_hero.name, secret_name=last_hero.secret_name)
    hero = crud.create_or_update_by_fields(
        hero, {"name": last_hero.name, "secret_name": last_hero.secret_name}
    )
    assert hero.id is not None
    assert hero.id == last_id
    assert hero.name == last_hero.name

    hero = HeroCreate(name="qwerty", secret_name=SECRET_NAME)
    hero = crud.create_or_update_by_fields(hero, {"name": "qwerty"})
    assert hero.id is not None
    print(last_id)
    print(hero.id)
    assert hero.id != last_id
    assert hero.name == "qwerty"

    hero = HeroCreate(name="NotExistentV2", secret_name=SECRET_NAME)
    with pytest.raises(HTTPException):
        crud.create_or_update_by_fields(hero, {"id": 1})
    with pytest.raises(HTTPException):
        crud.create_or_update_by_fields(hero, {"NotExistent": "NotExistent"})


def test_create_multiple():
    heroes = [
        HeroCreate(name="Hero1", secret_name="Secret1"),
        HeroCreate(name="Hero2", secret_name="Secret2"),
        HeroCreate(name="Hero3", secret_name="Secret3"),
    ]
    heroes = crud.create_multiple(heroes)
    assert len(heroes) == 3
    assert heroes[0].id is not None
    assert heroes[0].name == "Hero1"
    assert heroes[0].secret_name == "Secret1"
    assert heroes[0].age is None
    assert heroes[0].is_alive is True

    assert heroes[1].id is not None
    assert heroes[1].name == "Hero2"
    assert heroes[1].secret_name == "Secret2"
    assert heroes[1].age is None
    assert heroes[1].is_alive is True

    assert heroes[2].id is not None
    assert heroes[2].name == "Hero3"
    assert heroes[2].secret_name == "Secret3"
    assert heroes[2].age is None
    assert heroes[2].is_alive is True


def test_create_or_update_multiple_by_fields():
    heroes = [
        HeroCreate(name="Hero1", secret_name="Secret1"),
        HeroCreate(name="Hero2", secret_name="Secret2"),
        HeroCreate(name="Hero3", secret_name="Secret3"),
    ]
    heroes = crud.create_or_update_multiple_by_fields(heroes, {"name": "Hero1"})
    assert len(heroes) == 3
    assert heroes[0].id is not None
    assert heroes[0].name == "Hero1"
    assert heroes[0].secret_name == "Secret1"
    assert heroes[0].age is None
    assert heroes[0].is_alive is True

    assert heroes[1].id is not None
    assert heroes[1].name == "Hero2"
    assert heroes[1].secret_name == "Secret2"
    assert heroes[1].age is None
    assert heroes[1].is_alive is True

    assert heroes[2].id is not None
    assert heroes[2].name == "Hero3"
    assert heroes[2].secret_name == "Secret3"
    assert heroes[2].age is None
    assert heroes[2].is_alive is True

    heroes = [
        HeroCreate(name="Hero1", secret_name="Secret1"),
        HeroCreate(name="Hero2", secret_name="Secret2"),
        HeroCreate(name="Hero4", secret_name="Secret4"),
    ]
    heroes = crud.create_or_update_multiple_by_fields(heroes, ["name"])
    assert len(heroes) == 3
    assert heroes[0].id is not None
    assert heroes[0].name == "Hero4"
    assert heroes[0].secret_name == "Secret4"
    assert heroes[0].age is None
    assert heroes[0].is_alive is True

    assert heroes[1].id is not None
    assert heroes[1].name == "Hero1"
    assert heroes[1].secret_name == "Secret1"
    assert heroes[1].age is None
    assert heroes[1].is_alive is True

    assert heroes[2].id is not None
    assert heroes[2].name == "Hero2"
    assert heroes[2].secret_name == "Secret2"
    assert heroes[2].age is None
    assert heroes[2].is_alive is True
