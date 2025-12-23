from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Calendar, Event
from datetime import datetime

calendar_bp = Blueprint("calendar", __name__)

@calendar_bp.route("/calendars", methods=["POST"])
@jwt_required()
def create_calendar():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    calendar = Calendar(
        name=data["name"],
        owner_id=user_id
    )

    db.session.add(calendar)
    db.session.commit()

    return jsonify({
        "id": calendar.id,
        "name": calendar.name
    }), 201

@calendar_bp.route("/calendars", methods=["GET"])
@jwt_required()
def list_calendars():
    user_id = int(get_jwt_identity())
    calendars = Calendar.query.filter_by(owner_id=user_id).all()

    return jsonify([
        {"id": c.id, "name": c.name}
        for c in calendars
    ])

@calendar_bp.route("/calendars/<int:calendar_id>/events", methods=["POST"])
@jwt_required()
def create_event(calendar_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    calendar = Calendar.query.filter_by(
        id=calendar_id,
        owner_id=user_id
    ).first()

    if not calendar:
        return jsonify({"error": "Calendar not found"}), 404

    event = Event(
        calendar_id=calendar.id,
        title=data["title"],
        description=data.get("description"),
        start_time=datetime.fromisoformat(data["start_time"]),
        end_time=datetime.fromisoformat(data["end_time"]),
        created_by=user_id
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({
        "id": event.id,
        "title": event.title
    }), 201

@calendar_bp.route("/calendars/<int:calendar_id>/events", methods=["GET"])
@jwt_required()
def list_events(calendar_id):
    user_id = int(get_jwt_identity())

    calendar = Calendar.query.filter_by(
        id=calendar_id,
        owner_id=user_id
    ).first()

    if not calendar:
        return jsonify({"error": "Calendar not found"}), 404

    events = Event.query.filter_by(calendar_id=calendar.id).all()

    return jsonify([
        {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "start_time": e.start_time.isoformat(),
            "end_time": e.end_time.isoformat()
        }
        for e in events
    ])
