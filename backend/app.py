from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from config import SQLALCHEMY_DATABASE_URI
from extensions import db

app = Flask(__name__)
app.config.from_object("config")

db.init_app(app)   
migrate = Migrate(app, db)
jwt = JWTManager(app)

import models      
from auth import auth_bp
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return "Backend is running!"

if __name__ == "__main__":
    app.run(debug=True)
