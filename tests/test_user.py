import pytest
from flask_sqlalchemy import SQLAlchemy

from MVC.User.Model.User import User
from main import create_app
from db import db
from utils.DataValidator import convert_string_to_date


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        # add test data
        user = User(
            "plobanov",
            "plobanov@mail.ru",
            "PAVEL LOBANOV",
            "MALE",
            convert_string_to_date("2022-01-01"),
            "HSE",
            "88005553535",
            id=1)
        db.session.add(user)
        db.session.commit()
    
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 302


def test_create_user(client):
    response = client.post("/users/create", data={
        "password": "qwerty",
        "email": "a@mail.ru",
        "fio": "IVANOV IVAN",
        "sex": "Male",
        "date_of_birth": "2000-01-01",
        "source_of_knowing_about_pskk": "HSE",
        "phone_number": "88005553535"
    })

    assert response.status_code == 400