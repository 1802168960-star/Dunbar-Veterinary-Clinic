"""Home and health endpoints."""
from flask import Blueprint, abort, render_template

from app.models import Client, db
from app.services.scheduling import appointments_for_client

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.get("/clients/<int:client_id>/appointments")
def client_appointments(client_id):
    client_record = db.session.get(Client, client_id)
    if client_record is None:
        abort(404, description="Client not found.")

    return render_template(
        "client_appointments.html",
        client_record=client_record,
        appointments=appointments_for_client(client_id),
    )


@main_bp.get("/healthz")
def healthz():
    return {"status": "ok"}
