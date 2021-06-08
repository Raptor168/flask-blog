from flask import render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from db import db, app, Users


def get_name(name_id):
	name_id = Users.query.filter_by(id=name_id).first()
	if name_id is None:
		abort('404')
	else:
		return name_id


@app.route('/')
def index():
	names = Users.query.all()
	return render_template('index.html', names=names)


@app.route('/add', methods=('GET', 'POST'))
def add():
	if request.method == 'POST':
		name = request.form['user_name']

		if not name:
			flash('Name is required!')
		else:
			insert = Users(name=name)
			db.session.add(insert)
			db.session.commit()
			return redirect(url_for('index'))
	return render_template('add.html')


@app.route('/<int:name_id>')
def details(name_id):
	name = get_name(name_id)
	return render_template('details.html', name=name)


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
	name = get_name(id)
	edited = Users.query.filter_by(id=id).one()
	if request.method == 'POST':
		name = request.form['user_name']
		if not name:
			flash('Name is required!')
		else:
			edited.name = name
			db.session.add(edited)
			db.session.commit()
			return redirect(url_for('index'))
	return render_template('edit.html', name=name)


@app.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
	deleted = Users.query.filter_by(id=id).one()
	if request.method == 'POST':
		db.session.delete(deleted)
		db.session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('delete.html', name=deleted)


if __name__ == '__main__':
	app.run(debug=True)
