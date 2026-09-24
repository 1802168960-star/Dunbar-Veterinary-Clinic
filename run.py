"""Development entry point: python run.py

The interactive debugger stays off unless ``FLASK_DEBUG=1`` is set, so a
clinic machine never exposes it by accident.
"""
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0").strip().lower() not in ("", "0", "false", "no")
    app.run(debug=debug)
