from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService
from setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    john = Director(id=1, name='john')
    oliver = Director(id=2, name='oliver')
    wick = Director(id=3, name='wick')

    director_dao.get_one = MagicMock(return_value=john)
    director_dao.get_all = MagicMock(return_value=[john, oliver, wick])
    director_dao.create = MagicMock(return_value=Director(id=4, name='sam'))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) == 3
        assert len(directors) > 0

    def test_create(self):
        director_data = {
            "name": "sam"
        }
        director = self.director_service.create(director_data)
        assert director.name == director_data['name']

    def test_delete(self):
        director = self.director_service.delete(1)
        assert director is None

    def test_update(self):
        director_data = {
            "id": 3,
            "name": "lex",
        }
        self.director_service.update(director_data)
