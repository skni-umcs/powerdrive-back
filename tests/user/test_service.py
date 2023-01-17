from src.user.schemas import UserCreate, UserUpdate
from src.user.models import verify_password
from src.user.service import add, get_by_index, get_by_username, get_all, update, delete_by_index
from src.user.exceptions import UserNotFoundException
from sqlalchemy.exc import IntegrityError
from tests import get_db

import pytest


SESSION = get_db().__next__()


def test_add():
    user_in = UserCreate(
        username="string",
        first_name="String",
        last_name="String",
        email="string@string.string",
        password="String123.",
    )
    user = add(SESSION, user_in)
    pytest.user1 = user
    assert pytest.user1


def test_add_duplicate():
    user_in = UserCreate(
        username="string",
        first_name="String",
        last_name="String",
        email="string@string.string",
        password="String123.",
    )
    try:
        assert not add(SESSION, user_in)
    except IntegrityError:
        SESSION.rollback()


def test_get_by_index():
    user_id = pytest.user1.id
    user = get_by_index(SESSION, user_id)
    assert pytest.user1 == user


def test_get_by_index_fail():
    user_id = pytest.user1.id + 1
    try:
        assert not get_by_index(SESSION, user_id)
    except UserNotFoundException:
        assert True


def test_get_by_username():
    username = pytest.user1.username
    user = get_by_username(SESSION, username)
    assert pytest.user1 == user


def test_get_by_username_fail():
    username = pytest.user1.username + "1"
    try:
        assert not get_by_username(SESSION, username)
    except UserNotFoundException:
        assert True


def test_get_all():
    users = get_all(SESSION)
    assert pytest.user1 in users
    assert len(users) == 1


def test_update():
    user_in = UserUpdate(**pytest.user1.__dict__)
    user_in.username = "string2"
    user_in.first_name = "String2"
    user_in.last_name = "String2"
    user_in.email = "str@str.str"
    user_in.password = "String1234."
    user = update(SESSION, user_in)
    for key, value in user_in.dict().items():
        if key == "password":
            assert verify_password(value, getattr(user, key))
            continue
        assert getattr(user, key) == value
    pytest.user1 = user


def test_update_fail():
    user_in = UserUpdate(**pytest.user1.__dict__)
    user_in.id = pytest.user1.id + 1
    try:
        assert not update(SESSION, user_in)
    except UserNotFoundException:
        SESSION.rollback()


def test_delete_by_index():
    user_id = pytest.user1.id
    delete_by_index(SESSION, user_id)
    try:
        assert not get_by_index(SESSION, user_id)
    except UserNotFoundException:
        SESSION.rollback()


def test_delete_by_index_fail():
    user_id = pytest.user1.id
    try:
        assert delete_by_index(SESSION, user_id)
    except UserNotFoundException:
        SESSION.rollback()
