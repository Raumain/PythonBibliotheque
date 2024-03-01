import sqlite3
from flask import g
DATABASE = 'db/database'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


class User:
    def __init__(self, user_id, name, surname, mail, password, address):
        self._id = user_id
        self._name = name
        self._surname = surname
        self._mail = mail
        self._password = password
        self._address = address

    @staticmethod
    def get_all_users(db):
        query = "select * from User;"
        cur = db.execute(query)
        results = cur.fetchall()
        cur.close()

        users = []

        for r in results:
            user = User(r[0], r[1], r[2], r[3], r[4], r[5])
            users.append(user)

        return users
    
    @staticmethod
    def get_user_by_id_with_books(db, user_id):
        query = "SELECT b.title, l.date_start, l.date_end, l.book_id FROM Loan l JOIN Book b ON l.book_id = b.id WHERE l.user_id = ?;"
        cur = db.execute(query, [user_id])
        results = cur.fetchall()
        cur.close()
        return results
       
    @staticmethod
    def get_users_with_books(db):
        query = "select u.first_name, u.name, b.title, l.date_start, l.date_end, l.book_id from User u join Loan l on u.id = l.user_id join Book b on l.book_id = b.id;"
        cur = db.execute(query)
        results = cur.fetchall()
        cur.close()

        return results
       

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_by_id(self, user_id):
        query = "select * from User where id = ?;"
        cur = get_db().execute(query, [user_id])
        r = cur.fetchall()[0]
        cur.close()

        return User(r[0], r[1], r[2], r[3], r[4], r[5])

    @staticmethod
    def get_by_id_static(user_id):
        query = "select * from User where id = ?;"
        cur = get_db().execute(query, [user_id])
        r = cur.fetchall()[0]
        cur.close()

        return User(r[0], r[1], r[2], r[3], r[4], r[5])
