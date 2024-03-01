from flask import Flask, render_template, g, request, session, redirect, url_for
from flask_bcrypt import Bcrypt
from datetime import date
import sqlite3
import os
from classes.Loan import Loan
from classes.user import User
from classes.books import Book

DATABASE = 'db/database'

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)


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

    conn.close()
    return render_template('index.html', books=rows, session=session)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM User WHERE mail = ?', (mail,))
        user = cursor.fetchone()
        passwordDB = user[4]

        hashed_password_from_db = passwordDB
        entered_password = password

        if bcrypt.check_password_hash(hashed_password_from_db, entered_password):
            user_id = user[0]
            name = user[1]
            firstname = user[2]
            mail = user[3]
            role = user[6]

            session['user_id'] = user_id
            session['name'] = name
            session['firstname'] = firstname
            session['mail'] = mail
            session['role'] = role

            return redirect(url_for('index'))

    return render_template('login.html')


@app.route("/book/<int:book_id>")
def book(book_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Book WHERE id = ?', [book_id])
    book = cursor.fetchone()
    db.close()
    return render_template('book.html', book=book)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        firstname = request.form['firstname']
        address = request.form['address']
        mail = request.form['mail']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO User (name, first_name, address, mail, password, address, role) VALUES (?, ?, ?, ?, ?, ?, "user")', (name, firstname, address, mail, hashed_password, address))
        db.commit()

        return redirect(url_for('index'))

    return render_template('login.html')


@app.route("/admin", methods=['GET'])
def admin():
    if session.get('user_id') is None or session.get('role') != "admin":
        return redirect(url_for('index'))

    users_and_books = User.get_users_with_books(get_db())
    return render_template('admin.html', users=users_and_books)

@app.route("/profil", methods=['GET'])
def profil():
    if session.get('user_id') is None or session.get('role') != "user":
        return redirect(url_for('index'))

    users_and_books = User.get_user_by_id_with_books(get_db(), session.get('user_id'))
    return render_template('profil.html', users=users_and_books)


@app.route("/loan/<int:book_id>")
def loan_id(book_id):
    if session.get('user_id') is None:
        return redirect(url_for('index'))

    user = User(session.get('user_id'), session.get('name'), session.get('firstname'), '', '', '')
    books = Book.get_all_books(get_db())
    return render_template('loan.html', user=user, book_id=book_id, books=books)


@app.route("/end-loan/<int:book_id>")
def end_loan(book_id):
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('index'))

    loan = Loan.get_loan_by_book_id(book_id, user_id)
    print("loan id", loan.get_id())
    Loan.end_loan(get_db(), loan)
    return redirect(url_for('admin'))


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
    user_id = int(request.form.get('user_id'))
    book_id = int(request.form.get('book_id'))
    date_end = request.form.get('date_end')
    price = int(request.form.get('price'))

    new_loan = Loan(user_id, book_id, date.today().__str__(), date_end, price)
    Loan.create_loan(get_db(), new_loan)

    return redirect(url_for('index'))


@app.route('/register-book', methods=['GET', 'POST'])
def register_book():
    if request.method == 'POST':
        title = request.form['title']
        type = request.form['type']
        genre = request.form['genre']
        editor = request.form['editor']
        author = request.form['author']
        release_year = request.form['release_year']

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO Book (title, type, genre, editor, author, release_year, borrowed) VALUES (?, ?, ?, ?, ?, ?, false)',
            (title, type, genre, editor, author, release_year))
        db.commit()

        return redirect(url_for('index'))

    return render_template('book-form.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_query = request.form['search']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Book WHERE title LIKE ?', ('%' + search_query + '%',))
        search_results = cursor.fetchall()
        conn.close()

        if search_results:
            return render_template('index.html', books=search_results)
        else:
            return render_template('index.html', no_results=True)

    else:
        return redirect(url_for('index'))
