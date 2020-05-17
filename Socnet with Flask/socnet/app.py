from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "your_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:your_password@localhost/socnet"

db = SQLAlchemy(app)
