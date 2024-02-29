from flask import Flask, render_template, g, request, session, redirect, url_for
import sqlite3
import os
from classes.Loan import Loan

DATABASE = 'db/database'

app = Flask(__name__)
app.secret_key = os.urandom(24)


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
def index():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Book')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
    return render_template('index.html', books=rows)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM User WHERE mail = ? AND password = ?', (mail, password))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            name = user[1]
            firstname = user[2]
            mail = user[3]

            session['user_id'] = user_id
            session['name'] = name
            session['firstname'] = firstname
            session['mail'] = mail

            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        firstname = request.form['firstname']
        address = request.form['address']
        mail = request.form['mail']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO User (id, name, first_name, address, mail, password, address) VALUES (23, ?, ?, ?, ?, ?, ?)', (name, firstname, address, mail, password, address))
        db.commit()

        return redirect(url_for('index'))

    return render_template('login.html')

@app.route("/loan")
def loan():
    return render_template('loan.html')
  
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('firstname', None)
    session.pop('mail', None)
    return redirect(url_for('login'))


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
