from flask import Flask
from flask_migrate import Migrate
from extensions import db, jwt, socketio
import socket_events

app = Flask(__name__)
app.config.from_object("config")

db.init_app(app)   
jwt.init_app(app)
socketio.init_app(app)
migrate = Migrate(app, db)
    
from auth import auth_bp
from calendar_routes import calendar_bp

app.register_blueprint(auth_bp)
app.register_blueprint(calendar_bp)


@app.route("/")
def home():
    return "Backend is running!"

if __name__ == "__main__":
    socketio.run(app, debug=True)

