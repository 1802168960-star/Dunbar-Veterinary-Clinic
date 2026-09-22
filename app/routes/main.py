"""Home, appointment cancellation and health endpoints."""
from flask import Blueprint, abort, redirect, render_template, request, url_for

from app.models import Appointment, db
from app.services.scheduling import cancel_appointment as mark_cancelled

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.route("/appointments/<int:appointment_id>/cancel", methods=["GET", "POST"])
def cancel_appointment(appointment_id):
    appointment = db.session.get(Appointment, appointment_id)
    if appointment is None:
        abort(404, description="Appointment not found.")

    changed = False
    if request.method == "POST":
        changed = mark_cancelled(appointment)
        db.session.commit()
        return redirect(
            url_for(
                "main.cancel_appointment",
                appointment_id=appointment.id,
                changed="1" if changed else "0",
            )
        )

    return render_template(
        "cancel_appointment.html",
        appointment=appointment,
        changed=request.args.get("changed") == "1",
        already_cancelled=request.args.get("changed") == "0",
    )


@main_bp.get("/healthz")
def healthz():
    return {"status": "ok"}
