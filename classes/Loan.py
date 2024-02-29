class Loan:
    def __init__(self, _id=None, _user_id=None, _book_id=None, _date_start=None, _date_end=None, price_per_day=None):
        self._id = _id
        self._user_id = _user_id
        self._book_id = _book_id
        self._date_start = _date_start
        self._date_end = _date_end
        self._price_per_day = price_per_day
        self._total_price = 0

    @staticmethod
    def create_loan(db, loan):
        query = ("INSERT INTO loan (user_id, book_id, date_start, date_end, price, total_price) "
                 "VALUES (?, ?, ?, ?, ?, ?);")
        cur = db.execute(query,
                         [loan.get_user_id(), loan.get_book_id(), loan.get_date_start(), loan.get_date_end(),
                          loan.get_price_per_day(), loan.get_total_price()])
        rv = cur.fetchall()
        cur.close()
        print(rv)
        return True

    @staticmethod
    def end_loan(self):
        pass

    # SETTERS

    def set_id(self, loan_id):
        self._id = loan_id

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
