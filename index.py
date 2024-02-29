from flask import Flask, render_template, request, g
import sqlite3
from classes.Loan import Loan

DATABASE = 'db/database.db'

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/loan")
def loan():
    return render_template('loan.html')


# API
@app.route('/api/new-loan', methods=['POST'])
def CreateNewLoanEndpoint():
    book_id = request.form['book_id']
    user_id = request.form['user_id']
    date_start = request.form['date_start']
    date_end = request.form['date_end']
    price = request.form['price']

    new_loan = Loan(book_id, user_id, date_start, date_end, price)
    Loan.create_loan(get_db(), new_loan)

    return f'<h1>Emprunt enregistré !</a>'
