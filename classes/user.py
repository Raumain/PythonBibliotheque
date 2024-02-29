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
    def get_users_with_books(db):
        query = "select u.first_name, u.name, b.title, l.date_start, l.date_end from User u join Loan l on u.id = l.user_id join Book b on l.book_id = b.id;"
        cur = db.execute(query)
        results = cur.fetchall()
        cur.close()
        print('ok')
        print(results)

        return results
        
        
        
       

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id
