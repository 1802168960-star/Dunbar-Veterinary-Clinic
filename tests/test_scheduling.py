"""Unit tests for the consulting timetable rules."""
from datetime import date, time
from types import SimpleNamespace

from app.services.scheduling import (
    slots_for_day,
    validate_consultation,
    validate_farm_visit,
)

MONDAY = date(2026, 9, 21)
TUESDAY = date(2026, 9, 22)
SATURDAY = date(2026, 9, 26)
SUNDAY = date(2026, 9, 27)


def test_monday_runs_from_0830_to_1715_in_fifteen_minute_slots():
    slots = slots_for_day(MONDAY)
    assert slots[0] == time(8, 30)
    assert slots[-1] == time(17, 15)
    assert len(slots) == 36


def test_tuesday_consults_stop_after_1015():
    slots = slots_for_day(TUESDAY)
    assert slots[-1] == time(10, 15)
    assert time(10, 30) not in slots


def test_saturday_is_a_short_consulting_morning():
    slots = slots_for_day(SATURDAY)
    assert slots[0] == time(8, 0)
    assert slots[-1] == time(10, 45)


def test_sunday_is_closed():
    assert slots_for_day(SUNDAY) == []


def test_consultation_needs_an_animal_and_a_room():
    problems = validate_consultation(day=MONDAY, start=time(9, 0), animal=None, room=1)
    assert "A consultation must be booked for one animal." in problems

    problems = validate_consultation(day=MONDAY, start=time(9, 0), animal=object(), room=3)
    assert "A consultation must be booked into consulting room 1 or 2." in problems


def test_consultation_time_must_sit_on_the_timetable():
    problems = validate_consultation(day=MONDAY, start=time(9, 7), animal=object(), room=1)
    assert "That time is not a 15-minute slot on the consulting timetable." in problems


def test_a_room_cannot_hold_two_live_consultations():
    existing = [SimpleNamespace(status="booked", room=1, start_time=time(9, 0))]
    problems = validate_consultation(
        day=MONDAY, start=time(9, 0), animal=object(), room=1, existing_bookings=existing
    )
    assert "That consulting room is already booked for that slot." in problems


def test_cancelled_bookings_do_not_block_a_slot():
    existing = [SimpleNamespace(status="cancelled", room=1, start_time=time(9, 0))]
    problems = validate_consultation(
        day=MONDAY, start=time(9, 0), animal=object(), room=1, existing_bookings=existing
    )
    assert problems == []


def test_valid_consultation_has_no_problems():
    problems = validate_consultation(day=MONDAY, start=time(9, 0), animal=object(), room=2)
    assert problems == []


def test_farm_visit_needs_a_property():
    problems = validate_farm_visit(day=TUESDAY, start=time(11, 15), farm_property=None, estimated_hours=3)
    assert "A farm visit must be booked against a property." in problems


def test_farm_visit_duration_is_in_half_hour_steps():
    problems = validate_farm_visit(
        day=TUESDAY, start=time(11, 15), farm_property=object(), estimated_hours=1.25
    )
    assert "The estimated duration must be in half-hour steps." in problems


def test_farm_visit_can_start_outside_the_consulting_grid():
    problems = validate_farm_visit(
        day=TUESDAY, start=time(14, 45), farm_property=object(), estimated_hours=1.5
    )
    assert problems == []
