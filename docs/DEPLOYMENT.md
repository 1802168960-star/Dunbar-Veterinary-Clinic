# Deployment and configuration — Dunbar Veterinary Clinic appointment system

The clinic is a small practice on an unreliable internet connection, so the
system is deployed **on a machine inside the clinic**: a Python process and a
SQLite database file. Nothing in the application calls the internet at run
time.

## 1. What runs where

| Piece | Where it runs | Notes |
|---|---|---|
| Flask application | clinic PC or small server | `python run.py` for development, `wsgi:app` behind waitress/gunicorn otherwise |
| SQLite database | `instance/dunbar.sqlite3` | one file; copy it to back it up |
| Static files | served by the application | local CSS only, no CDN |

## 2. Configuration

Settings are read at start-up in this order — the first one that has a value wins:

1. real environment variables (set by the shell or the service manager);
2. the `.env` file next to `config.py` (copy `.env.example` to `.env`);
3. the defaults in `config.py`.

| Variable | Purpose | Default |
|---|---|---|
| `SECRET_KEY` | signs session cookies; change it on any shared machine | `dev-secret-key-change-me` |
| `DATABASE_URL` | SQLAlchemy connection string. Relative SQLite paths resolve inside `instance/` | `<project>/instance/dunbar.sqlite3` |
| `FLASK_DEBUG` | `1` turns the interactive debugger on (development only) | `0` |

`.env` is git-ignored; `.env.example` shows the shape and is safe to share.

## 3. First-time setup

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1
```

macOS / Linux:

```bash
bash scripts/bootstrap.sh
```

The scripts create `.venv`, install `requirements.txt`, copy `.env.example` to
`.env` when there is none, and seed the database with the case study's sample
data. `scripts/bootstrap.ps1 -ResetDatabase` rebuilds the sample data from
scratch.

The manual equivalent, if a script cannot be used:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # Windows
.venv/bin/python    -m pip install -r requirements.txt   # macOS / Linux
python scripts/seed_data.py
```

## 4. Running

| Situation | Command |
|---|---|
| Development, on this machine | `python run.py` (or `scripts\run.ps1` on Windows) |
| Small server on Windows | `waitress-serve --listen=127.0.0.1:8080 wsgi:app` |
| Small server on Linux | `gunicorn --bind 127.0.0.1:8080 wsgi:app` |

waitress and gunicorn are optional extras: `pip install waitress` or
`pip install gunicorn`. The application only needs to bind to the local
machine; the clinic does not expose it to the internet.

## 5. Tests and continuous integration

```bash
python -m pytest -q
```

GitHub Actions runs the same command on every pull request and on every push
to `main` (`.github/workflows/ci.yml`). A green run is part of the definition
of done for every story.

## 6. Data and backups

- The database is the single file `instance/dunbar.sqlite3` (path configurable
  with `DATABASE_URL`).
- Back it up by copying the file while the app is stopped, or with
  `sqlite3 instance/dunbar.sqlite3 ".backup backup.sqlite3"`.
- Deleting the file and running `python scripts/seed_data.py` rebuilds the
  sample data; there is no migration to run.

## 7. Releases and version numbers

- `CHANGELOG.md` follows Keep a Changelog; every merged story adds an entry.
- Tags: `v0.1` after Sprint 1, `v1.0` at handover. Tag the commit on `main`
  and summarise the changes in the GitHub release notes.
- Release steps: merge the pull request into `main` → tag → publish the
  release notes → make sure the changelog entry matches.

## 8. Troubleshooting

| Symptom | Fix |
|---|---|
| `Address already in use` | another copy is running; stop it or change the port in `run.py` |
| `no such table` | run `python scripts/seed_data.py` to create the database |
| Demo data has drifted | `python scripts/seed_data.py --reset` |
| `.env` changes seem ignored | the real environment wins over `.env`; check for an exported variable |
