"""Smoke tests: the application starts and serves the home page."""
from app.models import Animal, Client, db


def test_home_page_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"One appointment book for both halves of the practice" in response.data


def test_health_endpoint(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_client_and_animal_records_persist(app):
    with app.app_context():
        owner = Client(name="Mrs Prosser", phone="0417 552 118")
        owner.animals.append(Animal(name="Biscuit", species="Cat"))
        db.session.add(owner)
        db.session.commit()

        saved = Client.query.filter_by(name="Mrs Prosser").one()
        assert saved.phone == "0417 552 118"
        assert [animal.name for animal in saved.animals] == ["Biscuit"]
