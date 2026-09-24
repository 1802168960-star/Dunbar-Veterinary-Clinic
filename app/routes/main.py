"""Home and health endpoints."""
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.get("/healthz")
def healthz():
    return {"status": "ok"}
