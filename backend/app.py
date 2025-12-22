from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

@app.route("/")
def home():
    return "Backend is running!"

if __name__ == "__main__":
    app.run(debug=True)
