import pytest

from app import create_app
from app.models import db as _db


@pytest.fixture
def app(tmp_path):
    database_file = tmp_path / "test.sqlite3"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_file}",
        }
    )
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
