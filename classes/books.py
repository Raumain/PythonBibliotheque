from flask import g


# Je me connecte à la base de données
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


# J'exécute une requête SQL sur la base de données
def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    get_db().commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


class Book:
    def __init__(self, id, title, type, genre, editor, author, release_year, borrowed):
        self.id = id
        self.title = title
        self.type = type
        self.genre = genre
        self.editor = editor
        self.author = author
        self.release_year = release_year
        self.borrowed = borrowed

    @staticmethod
    def get_all_books(db):
        query = "select * from Book;"
        cur = db.execute(query)
        results = cur.fetchall()
        cur.close()

        books = []

        for r in results:
            book = Book(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
            books.append(book)

        return books

    @staticmethod
    def get_book_by_id_static(user_id):
        query = "select * from Book where id = ?;"
        cur = get_db().execute(query, [user_id])
        r = cur.fetchone()
        cur.close()

        return Book(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])

    def add_rent(self, borrower_name):
        # Je vérifie si le livre est déjà emprunté
        if self.borrowed:
            print(f"Le livre \"{self.title}\" est déjà emprunté.")
            return
        # Sinon, je met à jour la base de données pour marquer le livre comme emprunté
        query_db("UPDATE Book SET borrowed = 1 WHERE id = ?", [self.id])
        print(f"Le livre \"{self.title}\" a été loué à {borrower_name}.")

    def delete_rent(self, borrower_name):
        # Je vérifie si le livre est emprunté
        if not self.borrowed:
            print(f"Le livre \"{self.title}\" n'est pas actuellement emprunté.")
            return
        # Sinon, je met à jour la base de données pour marquer le livre comme non emprunté
        query_db("UPDATE Book SET borrowed = 0 WHERE id = ?", [self.id])
        print(f"La location du livre \"{self.title}\" pour {borrower_name} a été annulée.")

    def show_details(self):
        print(f"Titre: {self.title}")
        print(f"Auteur: {self.author}")
        print(f"Année de sortie: {self.release_year}")
        print(f"Type de livre: {self.type}")
        print(f"Genre du livre: {self.genre}")

        # Je récupère l'état d'emprunt du livre depuis la base de données
        borrowed_status = query_db("SELECT borrowed FROM Book WHERE id = ?", [self.id], one=True)
        if borrowed_status:
            borrowed = borrowed_status[0]
            print(f"Emprunté: {'Oui' if borrowed else 'Non'}")

    def get_id(self):
        return str(self.id)

    def get_title(self):
        return self.title
