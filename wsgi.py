"""WSGI entry point for a small production-style server.

The clinic runs the application on its own machine. On Windows:

    waitress-serve --listen=127.0.0.1:8080 wsgi:app

On Linux:

    gunicorn --bind 127.0.0.1:8080 wsgi:app
"""
from app import create_app

app = create_app()
