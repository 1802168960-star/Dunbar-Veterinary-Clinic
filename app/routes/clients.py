"""Client records: the register of households and farm businesses.

Story MSD426GXUST3-39. Nothing can be booked, a consultation in one of the two
rooms or a farm visit against a property, until the client is on file, so this
is the screen the front desk uses first. The rules live in
``app.services.records``; this module is the HTTP layer that turns the
registration form into a ``Client`` row and shows it back in the client list.
"""
from flask import Blueprint, redirect, render_template, request, url_for

from app.models import Client, db
from app.services.records import clean, validate_client

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


def _submitted():
    """The form values as sent, so a rejected form can be handed straight back."""
    return {
        "name": request.form.get("name", ""),
        "phone": request.form.get("phone", ""),
        "email": request.form.get("email", ""),
        "postal_address": request.form.get("postal_address", ""),
        "notes": request.form.get("notes", ""),
        "sms_consent": request.form.get("sms_consent") == "on",
    }


@clients_bp.get("/")
def list_clients():
    """The client list, in the order the paper register is kept: by name."""
    clients = Client.query.order_by(db.func.lower(Client.name)).all()
    added_id = request.args.get("added", type=int)
    added = db.session.get(Client, added_id) if added_id else None
    return render_template("clients/list.html", clients=clients, added=added)


@clients_bp.get("/new")
def new_client():
    """Show the client registration form."""
    return render_template("clients/create.html", chosen={}, problems=[])


@clients_bp.post("/new")
def create_client():
    """Create the client record, or hand the form back with the problems."""
    chosen = _submitted()
    problems = validate_client(
        name=chosen["name"],
        phone=chosen["phone"],
        email=chosen["email"],
        postal_address=chosen["postal_address"],
    )
    if problems:
        # 400: the request was understood, the details are just not usable yet.
        return render_template("clients/create.html", chosen=chosen, problems=problems), 400

    record = Client(
        name=clean(chosen["name"]),
        phone=clean(chosen["phone"]),
        email=clean(chosen["email"]) or None,
        postal_address=clean(chosen["postal_address"]) or None,
        notes=clean(chosen["notes"]) or None,
        sms_consent=chosen["sms_consent"],
    )
    db.session.add(record)
    db.session.commit()

    return redirect(url_for("clients.list_clients", added=record.id), code=303)
