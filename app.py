from flask import Flask, render_template, g, request
import sqlite3
from datetime import datetime

app = Flask(__name__) #instantiate


def connect_db():
	sql = sqlite3.connect('/home/vagrant/src/ALL_PROJ/Projects PPrinted/EatFood/food_log.db')
	sql.row_factory = sqlite3.Row # dictionaries instead of tuples (simpler)
	return sql


def get_db():
	if not hasattr(g, 'sqlite3_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db
 
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
	db = get_db()
	if request.method == 'POST':
		date = request.form['date']

		dt = datetime.strptime(date, '%Y-%m-%d')
		database_date = datetime.strftime(dt, '%Y%m%d')

		db.execute('insert into log_date (entry_date) values (?)', [database_date])
		db.commit()

	cur = db.execute('select entry_date from log_date order by entry_date desc')
	results = cur.fetchall()

	face_results = []

	for i in results:
		single_date = {}

		d = datetime.strptime(str(i['entry_date']), '%Y%m%d')
		single_date['entry_date'] = datetime.strftime(d, '%B %d %Y')

		face_results.append(single_date)


	return render_template('home.html', results=face_results)


@app.route('/view/<date>', methods=['GET', 'POST'])   # 20170520 format
def view(date):
	if request.method == 'POST':
		return '<h1> The food item added is #{}</h1>'.format(request.form["food-select"])

	db = get_db()

	cur = db.execute('select entry_date from log_date where entry_date = ?', [date])
	result =  cur.fetchone()

	# return '<h1>The date is {}</h1>'.format(result['entry_date']) # test
	d = datetime.strptime(str(result['entry_date']), '%Y%m%d')
	face_date = datetime.strftime(d, '%B %d, %Y')

	food_cur = db.execute('select id, name from food')
	food_results = food_cur.fetchall()


	return render_template('day.html', date=face_date, food_results=food_results)

@app.route('/food', methods=['GET', 'POST'])
def food():

	db = get_db()   # initialize db

	if request.method == 'POST':
		name = request.form['food-name']
		protein = int(request.form['protein'])
		carbs = int(request.form['carbs'])
		fat = int(request.form['fat'])

		calories = protein * 4 + carbs * 4 + fat * 9

		db = get_db()   # initialize db
#next specify columns
		db.execute('insert into food (name, protein, carbs, fat, calories) values (?, ?, ?, ?, ?)', \
			[name, protein, carbs, fat, calories])
		db.commit() 
		# creat alert box here to test if necessary

		# return '<h1>Name: {} Protein: {} Carbs: {} Fat: {}</h1>'.format(request.form['food-name'], \ #  test submission
		# 	request.form['protein'], request.form['carbs'], request.form['fat'])   

	cur = db.execute('select name, protein, carbs, fat, calories from food')
	results = cur.fetchall()


		                   #   <--- to test only
	return render_template('add_food.html', results=results)


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)















