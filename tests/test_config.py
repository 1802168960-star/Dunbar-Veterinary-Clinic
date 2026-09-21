"""The .env loader behind the deployment configuration."""
import os

from config import load_env_file


def test_values_are_loaded_from_the_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "SECRET_KEY=from-file\nDATABASE_URL=sqlite:///demo.sqlite3\n", encoding="utf-8"
    )
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    loaded = load_env_file(env_file)

    assert loaded["SECRET_KEY"] == "from-file"
    assert loaded["DATABASE_URL"] == "sqlite:///demo.sqlite3"
    assert os.environ["SECRET_KEY"] == "from-file"


def test_the_real_environment_wins_over_the_file(tmp_path, monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "from-shell")
    env_file = tmp_path / ".env"
    env_file.write_text("SECRET_KEY=from-file\n", encoding="utf-8")

    load_env_file(env_file)

    assert os.environ["SECRET_KEY"] == "from-shell"


def test_comments_blank_lines_and_quotes_are_handled(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "# a comment\n\nSECRET_KEY=\"quoted value\"\nNOT_A_PAIR\n", encoding="utf-8"
    )
    monkeypatch.delenv("SECRET_KEY", raising=False)

    loaded = load_env_file(env_file)

    assert loaded == {"SECRET_KEY": "quoted value"}


def test_a_missing_file_is_fine(tmp_path):
    assert load_env_file(tmp_path / "not-here.env") == {}
