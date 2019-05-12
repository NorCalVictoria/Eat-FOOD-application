from flask import Flask, render_template, g , request
import sqlite3
app = Flask(__name__) #instantiate


def connect_db():
	sql = sqlite3.connect('~/src/ALL_PROJ/Projects PPrinted/EatFood/food_log.db')
	sql.row_factory = sqlite3.Row
	return sql


def get_db():
	if not hasattr(g, 'sqlite3_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
	

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/view')
def view():
	return render_template('day.html')

@app.route('/food', methods=['GET', 'POST'])
def food():
	if request.method == 'POST':
		name = int(request.form['food-name'])
		protein = int(request.form['protein'])
		carbs = int(request.form['carbs'])
		fat = int(request.form['fat'])

		calories = protein * 4 + carbs * 4 + fats * 9

		db = get_db #initialize db
		db.execute('insert into food (name, protein, carbs, fat, calories) values (?, ?, ?, ?, ?)', \
			[name, protein, carbs, fat, calories])
		db.commit()

		return '<h1>Name: {} Protein: {} Carbs: {} Fat: {}</h1>'.format(request.form['food-name'], \
			request.form['protein'], request.form['carbs'], request.form['fat'])
	return render_template('add_food.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)















