import sqlite3


class Loan:
    def __init__(self, _id, _user_id, _book_id, _date_start, _date_end, price_per_day):
        self._id = _id
        self._user_id = _user_id
        self._book_id = _book_id
        self._date_start = _date_start
        self._date_end = _date_end
        self._price_per_day = price_per_day
        self._total_price = 0

    # SETTERS

    def create_loan(self):
        # tentative de faire une query SQL
        query = "INSERT INTO loan () VALUES (?, ?)"
        cur = get_db().execute(query, [self._id, self._price_per_day])
        rv = cur.fetchall()
        cur.close()
        print(rv)
        return True

    def end_loan(self):
        pass

    def set_id(self, id):
        self._id = id

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
        return self._id

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
