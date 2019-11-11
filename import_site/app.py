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
	utils.create_new_user('team17', '406262515')
	utils.add_user_to_contest(4, 2)
	# utils.delete_all_imported_users()
	return 'Go to see the console'

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
