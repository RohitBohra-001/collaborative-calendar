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
