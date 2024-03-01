from classes.user import User
from classes.books import Book
import sqlite3
from flask import g

DATABASE = 'db/database'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


class Loan:
    def __init__(self, _user_id=None, _book_id=None, _date_start=None, _date_end=None, price_per_day=None):
        self._loan_id = 0
        self._user_id = _user_id
        self._book_id = _book_id
        self._date_start = _date_start
        self._date_end = _date_end
        self._price_per_day = price_per_day
        self._total_price = 0

    @staticmethod
    def create_loan(db, loan):
        query = ("INSERT INTO Loan (user_id, book_id, date_start, date_end, price, total_price) "
                 "VALUES (?, ?, ?, ?, ?, ?);")

        cur = db.execute(query,
                         [int(loan.get_user_id()), int(loan.get_book_id()), loan.get_date_start(), loan.get_date_end(),
                          float(loan.get_price_per_day()), float(loan.get_total_price())])
        db.commit()

        user = User.get_by_id_static(int(loan.get_user_id()))
        book = Book.get_book_by_id_static(int(loan.get_book_id()))
        book.add_rent(user.get_name())
        rv = cur.fetchall()
        cur.close()
        return True

    @staticmethod
    def end_loan(db, loan):
        query = "delete from Loan where id = ?"

        cur = db.execute(query,
                         [loan.get_id()])
        db.commit()

        user = User.get_by_id_static(int(loan.get_user_id()))
        book = Book.get_book_by_id_static(int(loan.get_book_id()))
        book.delete_rent(user.get_name())

    @staticmethod
    def get_loan_by_book_id(book_id, user_id):
        query = "select * from Loan where book_id = ? and user_id = ?;"
        cur = get_db().execute(query, [book_id, user_id])
        r = cur.fetchone()
        cur.close()

        loan = Loan(r[1], r[2], r[3], r[4], r[5])
        loan.set_id(r[0])
        return loan

    # SETTERS

    def set_id(self, loan_id):
        self._loan_id = loan_id

    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_book_id(self, book_id):
        self._book_id = book_id

    def set_date_start(self, date_start):
        self._date_start = date_start

    def set_date_end(self, date_end):
        self._date_end = date_end

    def set_price_per_day(self, price_per_day):
        self._price_per_day = price_per_day

    def set_total_price(self, total_price):
        self._total_price = total_price

    # GETTERS

    def get_id(self):
        return self._loan_id

    def get_user_id(self):
        return self._user_id

    def get_book_id(self):
        return self._book_id

    def get_date_start(self):
        return self._date_start

    def get_date_end(self):
        return self._date_end

    def get_price_per_day(self):
        return self._price_per_day

    def get_total_price(self):
        return self._total_price
