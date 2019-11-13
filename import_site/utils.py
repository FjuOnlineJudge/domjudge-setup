import os
from db import db
from sqlalchemy.sql import text

# This will fucked up in the log
def gen_password_hash(s):
	passwd = os.popen('php gen_pass.php {}'.format(s))
	return passwd.read()

def get_new_teamid():
	res = db.session.execute('SELECT teamid FROM team ORDER BY teamid DESC LIMIT 1')
	res = res.fetchone()[0]
	return res+1

def get_new_userid():
	res = db.session.execute('SELECT userid FROM user ORDER BY userid DESC LIMIT 1')
	res = res.fetchone()[0]
	return res+1

def create_new_user(username, passwd, name=None, email=None):
	name = name or username
	email = email or '{}@mail.fju.edu.tw'.format(passwd)

	teamid = get_new_teamid()
	userid = get_new_userid()
	# Keep the record
	sql = text('INSERT INTO import_users (uid, tid) VALUES (:uid, :tid)')
	res = db.session.execute(sql, {'uid': userid, 'tid': teamid})
	# Insert new team
	sql = text('INSERT INTO team (teamid, name,categoryid,members) VALUES (:tid, :name, :catid, :members);')
	res = db.session.execute(sql, {'tid': teamid, 'name': name, 'catid': 3, 'members': name})
	# Insert new user
	passwd = gen_password_hash(passwd) # hash
	sql = text('''
		INSERT INTO user (userid, username, name, email, password, teamid)
		VALUES (:uid, :username, :name, email, :passwd, :tid);
		''')
	res = db.session.execute(sql, {'uid': userid, 'username': username, 'name': name, 'email': email, 'passwd': passwd, 'tid': teamid})
	# Insert new userrole
	sql = text('INSERT INTO userrole (userid, roleid) VALUES (:uid, :rid);')
	res = db.session.execute(sql, {'uid': userid, 'rid': 3}) # normal user (looking for the docs)

	# db.session.commit()
	return {'uid': userid, 'tid': teamid}

def add_team_to_contest(tid, cid):
	sql = text('INSERT INTO contestteam (cid, teamid) VALUES (:cid, :tid)')
	res = db.session.execute(sql, {'cid': cid, 'tid': tid})
	if not res: # TODO(roy4801): ugly
		print(db.error)
		return False
	db.session.commit()
	return True

def add_user_to_contest(uid, cid):
	tid = db.session.execute('SELECT teamid from user WHERE userid=:uid', {'uid':uid}).first()
	if not tid:
		print('[*] tid is null in utils.add_user_to_contest')
		return
	tid = tid[0] # extract from tuple
	# Insert a contest team
	return add_team_to_contest(tid, cid)

def get_contest_list():
	sql = text('SELECT cid, name FROM contest')
	res = db.session.execute(sql)
	if res.returns_rows:
		li = res.fetchall()
	# print(li)
	return li

# TODO(roy4801): complete the functionality
def delete_all_imported_users():
	def del_user(uid):
		del_user = text('DELETE FROM user WHERE userid=:uid')
		del_userrole = text('DELETE FROM userrole WHERE userid=:uid')
		db.session.execute(del_user, {'uid': uid})
		db.session.execute(del_userrole, {'uid': uid})
	def del_team(tid):
		del_team = text('DELETE FROM team WHERE teamid=:tid')
		del_contestteam = text('DELETE FROM contestteam WHERE teamid=:tid')
		db.session.execute(del_team, {'tid': tid})
		db.session.execute(del_contestteam, {'tid': tid})
	def del_contestteam(tid):
		del_ctt = text('DELETE FROM contestteam WHERE teamid=:tid')
		db.session.execute(delctt, {'tid', tid})
	def del_import_users():
		del_import = text('DELETE FROM import_users')
		db.session.execute(del_import)

	li = text('SELECT uid, tid FROM import_users')
	res = db.session.execute(li)
	res = [(int(x), int(y)) for x, y in res]
	for uid, tid in res:
		print(uid, tid)
		del_user(uid)
		del_team(tid)
		del_contestteam(tid)
		del_import_users()
	# db.session.commit()
