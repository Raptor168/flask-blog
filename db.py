from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(90), nullable=False)