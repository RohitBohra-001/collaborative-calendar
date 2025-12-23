from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Calendar, Event, EventParticipant, User
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

@calendar_bp.route("/events/<int:event_id>/participants", methods=["POST"])
@jwt_required()
def add_participant(event_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    event = Event.query.filter_by(
        id=event_id,
        created_by=user_id
    ).first()

    if not event:
        return jsonify({"error": "Event not found or not authorized"}), 404

    participant_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not participant_user:
        return jsonify({"error": "User not found"}), 404

    existing = EventParticipant.query.filter_by(
        user_id=participant_user.id,
        event_id=event.id
    ).first()

    if existing:
        return jsonify({"error": "User already invited"}), 400

    participant = EventParticipant(
        user_id=participant_user.id,
        event_id=event.id,
        response="maybe"
    )

    db.session.add(participant)
    db.session.commit()

    return jsonify({"message": "User invited"}), 201

@calendar_bp.route("/events/<int:event_id>/participants", methods=["GET"])
@jwt_required()
def list_participants(event_id):
    user_id = int(get_jwt_identity())
    event = Event.query.filter_by(id=event_id).first()

    if not event:
        return jsonify({"error": "Event not found"}), 404

    if event.created_by != user_id:
        return jsonify({"error": "Not authorized"}), 403

    participants = EventParticipant.query.filter_by(
        event_id=event.id
    ).all()

    return jsonify([
        {
            "user_id": p.user_id,
            "response": p.response
        }
        for p in participants
    ])

@calendar_bp.route("/events/<int:event_id>/response", methods=["PATCH"])
@jwt_required()
def respond_to_event(event_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    participant = EventParticipant.query.filter_by(
        event_id=event_id,
        user_id=user_id
    ).first()

    if not participant:
        return jsonify({"error": "Not invited to this event"}), 404

    if data["response"] not in ["yes", "no", "maybe"]:
        return jsonify({"error": "Invalid response"}), 400

    participant.response = data["response"]
    db.session.commit()

    return jsonify({"message": "Response updated"})
