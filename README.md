# Dunbar Veterinary Clinic — Appointment System

A small web application for **ISYS3001 Managing Software Development** (Southern Cross University),
based on Case Study 5: *Dunbar Veterinary Clinic*.

The clinic currently books everything on a single paper appointment book (in-clinic
consultations) and a green diary (farm visits). This project delivers one appointment
system that holds both kinds of work, so the front desk, the vets and the owner can all
see the same day.

## Team

| GitHub account | Notes |
|---|---|
| [@mak1noo](https://github.com/mak1noo) | project owner |
| [@1802168960-star](https://github.com/1802168960-star) | team member |
| [@Codesprout-91](https://github.com/Codesprout-91) | team member |

## Tech stack

- Python 3 + Flask
- SQLite (local database file, no server required)
- pytest for automated tests
- No CDN or external services: the application must work when the clinic's internet is down

## Planned scope (Sprint 1)

- Clients, animals and farm properties: create, find, update, deactivate
- Two kinds of appointments:
  - in-clinic consultation: 15-minute slot, one animal, one of two consulting rooms
  - farm visit: booked against a property, start time + estimated hours
- Day views: consulting timetable (taken and free slots), farm run list, client appointments
- Reschedule and cancel (cancelled appointments stay visible in the record)

Out of scope for this project (kept in the product backlog): clinical records,
prescriptions and the drug register, invoicing, vaccination reminders, SMS/email,
client self-booking, surgery/theatre list, route planning, after-hours roster, stock,
and VetLedger data migration.

## Repository conventions

- `main` is the protected branch; all work arrives through pull requests.
- Branch names: `story/<JIRA-KEY>-short-name` (one branch per user story).
- Commit messages follow Conventional Commits: `feat:`, `fix:`, `test:`, `docs:`, `chore:`.
- Every pull request is reviewed by another team member before merging.
- Every user story carries automated tests; the Definition of Done is fixed by the unit.

## Running the application

Setup and run instructions are completed with the project scaffold in Sprint 1
(virtual environment, dependencies, seed data, tests).

## Links

- Jira project: _to be added_
- Confluence space: _to be added_
