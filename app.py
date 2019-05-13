from flask import Flask, render_template, g, request
import sqlite3

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
	

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/view')
def view():
	return render_template('day.html')

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
    
		# return '<h1>Name: {} Protein: {} Carbs: {} Fat: {}</h1>'.format(request.form['food-name'], \ #      test submission
		# 	request.form['protein'], request.form['carbs'], request.form['fat'])   

	cur = db.execute('select name, protein, carbs, fat, calories from food')
	results = cur.fetchall()


		                   #   <--- to test only
	return render_template('add_food.html', results=results)


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)















