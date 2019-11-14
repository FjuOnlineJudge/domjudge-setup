from flask import Flask, render_template, request
from sqlalchemy import text
#
from db import db
import config
import utils

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

def split_from_csv(content):
	# Split the user list
	user_list = []
	for i in content.split():
		t = i.split(',')
		if 'team' not in t[0]:
			t[0] = 'team' + t[0]
		user_list.append(tuple(t))
	return user_list

# TODO(roy4801): add the flash card
@app.route('/', methods=['GET', 'POST'])
def index():
	contests = utils.get_contest_list()
	users = ''
	#
	if request.method == 'POST':
		contest = request.form['contest'] if 'contest' in request.form else None
		users = request.form['users'] if 'users' in request.form else None
		del_flag = True if 'delete' in request.form else False
		print(contest, users, del_flag)
		if del_flag:
			utils.delete_all_imported_users()
			return render_template('index.html', contests=contests, text=users)

		user_list = split_from_csv(users)
		# Create the users
		cnt = 0
		for i in user_list:
			res = utils.create_new_user(i[0], i[1]) # username, password
			if res['uid'] and res['tid']:
				cnt += 1
	return render_template('index.html', contests=contests, text=users)
	# TODO(roy4801): store selected state (, selected=contest)
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
