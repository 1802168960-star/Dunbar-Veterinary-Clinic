"""Tests for cancelling appointments without deleting them (MSD426GXUST3-54)."""
from datetime import date, time

from app.models import (
    CONSULTATION,
    STATUS_BOOKED,
    STATUS_CANCELLED,
    Animal,
    Appointment,
    Client,
    db,
)
from app.services.scheduling import cancel_appointment


DAY = date(2026, 9, 21)


def _appointments():
    owner = Client(name="Mrs Prosser", phone="0417 552 118")
    animal = Animal(client=owner, name="Biscuit", species="Cat")
    first = Appointment(
        kind=CONSULTATION,
        status=STATUS_BOOKED,
        client=owner,
        animal=animal,
        date=DAY,
        start_time=time(9, 0),
        room=1,
        reason="Vaccination",
    )
    second = Appointment(
        kind=CONSULTATION,
        status=STATUS_BOOKED,
        client=owner,
        animal=animal,
        date=DAY,
        start_time=time(9, 15),
        room=1,
        reason="Recheck",
    )
    db.session.add(owner)
    db.session.add_all([first, second])
    db.session.commit()
    return first, second


def test_cancelling_keeps_the_record_and_changes_status(app):
    with app.app_context():
        first, _ = _appointments()
        assert cancel_appointment(first) is True
        db.session.commit()

        saved = db.session.get(Appointment, first.id)
        assert saved is not None
        assert saved.status == STATUS_CANCELLED


def test_cancelling_one_appointment_does_not_affect_another(app):
    with app.app_context():
        first, second = _appointments()
        cancel_appointment(first)
        db.session.commit()

        assert first.status == STATUS_CANCELLED
        assert second.status == STATUS_BOOKED


def test_cancelling_an_already_cancelled_appointment_is_idempotent(app):
    with app.app_context():
        first, _ = _appointments()
        assert cancel_appointment(first) is True
        assert cancel_appointment(first) is False
        db.session.commit()

        assert first.status == STATUS_CANCELLED


def test_cancel_page_shows_the_existing_record(app, client):
    with app.app_context():
        first, _ = _appointments()
        appointment_id = first.id

    response = client.get(f"/appointments/{appointment_id}/cancel")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Cancel appointment" in page
    assert "Mrs Prosser" in page
    assert "Booked" in page
    assert "Cancel this appointment" in page


def test_cancel_post_keeps_record_and_redirects(app, client):
    with app.app_context():
        first, second = _appointments()
        appointment_id = first.id
        second_id = second.id

    response = client.post(
        f"/appointments/{appointment_id}/cancel",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("changed=1")
    with app.app_context():
        cancelled = db.session.get(Appointment, appointment_id)
        unaffected = db.session.get(Appointment, second_id)
        assert cancelled.status == STATUS_CANCELLED
        assert unaffected.status == STATUS_BOOKED


def test_cancel_page_marks_cancelled_records_as_distinguishable(app, client):
    with app.app_context():
        first, _ = _appointments()
        first.status = STATUS_CANCELLED
        db.session.commit()
        appointment_id = first.id

    page = client.get(f"/appointments/{appointment_id}/cancel?changed=0").get_data(as_text=True)

    assert "Cancelled" in page
    assert "already cancelled" in page
    assert "stay visible" in page
    assert "Cancel this appointment" not in page


def test_cancel_unknown_appointment_is_404(client):
    assert client.get("/appointments/99999/cancel").status_code == 404
