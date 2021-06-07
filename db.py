from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/mydb'
db = SQLAlchemy(app)


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(90), nullable=False)
