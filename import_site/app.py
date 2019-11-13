from flask import Flask, render_template
from db import db
import config

import utils

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/test')
def test():
	s = None
	with open('list.csv', 'r') as f:
		s = f.readlines()
	li = []
	for i in s:
		row = i.split(',')
		li.append((row[0], row[1].rstrip()))

	for user, passwd in li:
		utils.create_new_user('team'+user, passwd)
	# utils.create_new_user('team17', '406262515')
	# utils.add_user_to_contest(4, 2) # uid cid
	# utils.delete_all_imported_users()
	return 'Success'

@app.route('/add')
def add():
	from sqlalchemy import text
	sql = text('INSERT INTO contestteam (cid, teamid) VALUES (:cid, :tid)')
	for i in range(6, 43):
		print(i)
		db.session.execute(sql, {'cid': 3, 'tid': i})
	db.session.commit()
	return 'Success'

@app.route('/delall')
def del_all():
	utils.delete_all_imported_users()
	return 'Success'

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
