class Books:
    def __init__(self, id, title, type, editor, author, release_year, borrowers):
        self.id = id
        self.title = title
        self.type = type
        self.editor = editor
        self.author = author
        self.release_year = release_year
        self.borrowers = borrowers

    def add_rent(self, borrower_name):
        self.borrowers.append(borrower_name)
        print(f"Le livre \"{self.title}\" a été loué à {borrower_name}.")

    def delete_rent(self, borrower_name):
        if borrower_name in self.borrowers:
            self.borrowers.remove(borrower_name)
            print(f"La location du livre \"{self.title}\" pour {borrower_name} a été annulée.")
        else:
            print(f"{borrower_name} n'a pas loué le livre \"{self.title}\".")

    def show_details(self):
        print(f"Titre: {self.title}")
        print(f"Auteur: {self.author}")
        print(f"Année de sortie: {self.release_year}")


# Valeurs pour créer un objet de ma classe Books
id = 1
title = "Le Seigneur des Anneaux"
type = "Fantasy"
editor = "Houghton Mifflin"
author = "J.R.R. Tolkien"
release_year = 1954
borrowers = []

# Création de l'objet de la classe Books
my_book = Books(id, title, type, editor, author, release_year, borrowers, )

# Appel de la méthode show_details de mon objet books
my_book.show_details()

# Ajouter une location
my_book.add_rent("Alice")

# Supprimer une location
my_book.delete_rent("Bob")
