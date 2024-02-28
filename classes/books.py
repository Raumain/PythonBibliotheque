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
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

class Books:
    def __init__(self, id, title, type, genre, editor, author, release_year, borrowed):
        self.id = id
        self.title = title
        self.type = type
        self.genre = genre
        self.editor = editor
        self.author = author
        self.release_year = release_year
        self.borrowed = borrowed

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

# Je créer une instance de la classe Books
my_book = Books(id=1, title="Le Seigneur des Anneaux", type="Roman", genre="Fantasy", editor="Houghton Mifflin", author="J.R.R. Tolkien", release_year=1954, borrowed=False)

# J'affiche les détails du livre
my_book.show_details()

# J'ajoute une location
my_book.add_rent("Alice")

# Je supprime une location
my_book.delete_rent("Bob")
