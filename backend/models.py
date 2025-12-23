from datetime import datetime, timezone
from passlib.hash import bcrypt
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    def set_password(self, password):
        from passlib.hash import bcrypt
        self.password_hash = bcrypt.hash(password)
    def check_password(self, password):
        from passlib.hash import bcrypt
        return bcrypt.verify(password, self.password_hash)

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(
        db.Integer,
        db.ForeignKey("calendar.id"),
        nullable=False
    )
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    version_number = db.Column(db.Integer, nullable=False, default=1)

class EventParticipant(db.Model):
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True
    )
    event_id = db.Column(
        db.Integer,
        db.ForeignKey("event.id"),
        primary_key=True
    )
    response = db.Column(
        db.String(20),
        nullable=False,
        default="maybe"
    )

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
