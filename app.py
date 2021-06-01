from flask import Flask
from flask import render_template, request, url_for, flash, redirect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sys

from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
Base = declarative_base()

engine = create_engine('mysql+mysqlconnector://root:root@localhost/mydb')


class Users(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	name = Column(Text, unique=False, nullable=False)


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_name(name_id):
	name_id = session.query(Users).filter_by(id=name_id).first()
	if name_id is None:
		abort('404')
	else:
		return name_id


@app.route('/')
def index():
	names = session.query(Users).all()
	return render_template('index.html', names=names)


@app.route('/add', methods=('GET', 'POST'))
def add():
	if request.method == 'POST':
		name = request.form['user_name']
		
		if not name:
			flash('Name is required!')
		else:
			insert = Users(name=name)
			session.add(insert)
			session.commit()
			return redirect(url_for('index'))
	return render_template('add.html')


@app.route('/<int:name_id>')
def details(name_id):
	name = get_name(name_id)
	return render_template('details.html', name=name)


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
	name = get_name(id)
	edited = session.query(Users).filter_by(id=id).one()
	if request.method == 'POST':
		name = request.form['user_name']
		if not name:
			flash('Name is required!')
		else:
			edited.name = name
			session.add(edited)
			session.commit()
			return redirect(url_for('index'))
	return render_template('edit.html', name=name)


@app.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
	deleted = session.query(Users).filter_by(id=id).one()
	if request.method == 'POST':
		session.delete(deleted)
		session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('delete.html', name=deleted)


if __name__ == '__main__':
	app.run(debug=True)
