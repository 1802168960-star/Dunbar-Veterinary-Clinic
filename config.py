"""Application configuration.

The application runs locally with a SQLite database file; no external service
is required, so the clinic keeps working when its internet connection drops.

Settings come from, in order of precedence:

1. real environment variables (set by the shell or the service manager);
2. a ``.env`` file next to this file — copy ``.env.example`` to ``.env``;
3. the defaults below.

``.env`` is git-ignored, so each machine keeps its own key and database path.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_env_file(path=None):
    """Read KEY=VALUE lines from ``path`` into the environment.

    Values that are already set always win, so a real environment variable
    overrides the file. Blank lines, comments and lines without ``=`` are
    ignored. Returns the pairs that were found, which keeps it easy to test.
    """
    path = Path(path) if path is not None else BASE_DIR / ".env"
    loaded = {}
    if not path.is_file():
        return loaded
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue
        loaded[key] = value
        os.environ.setdefault(key, value)
    return loaded


load_env_file()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'dunbar.sqlite3'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CREATE_TABLES_ON_START = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    CREATE_TABLES_ON_START = True


CONFIG_MAP = {
    "default": Config,
    "test": TestConfig,
}
