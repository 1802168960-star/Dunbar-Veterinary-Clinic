"""Application configuration.

The application runs locally with a SQLite database file; no external service
is required, so the clinic keeps working when its internet connection drops.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


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
