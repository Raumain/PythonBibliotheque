from classes.books import Book

# On créer une nouvelle classe 'Manga' qui hérite de la classe 'Book'
# Cette classe hérite des propritétées de 'Book', et rajoute la propriété `illustrator_name`, qui est spécifique aux mangas


class Manga(Book):
    def __init__(self, illustrator_name):
        super().__init__(self.get_id(), self.get_title(), self.get_type(), self.get_genre(), self.get_editor(), self.get_author(), self.get_release_year(), self.get_borrowed())
        self._illustrator_name = illustrator_name

    def get_illustrator_name(self):
        return self._illustrator_name

    def set_illustrator_name(self, illustrator_name):
        self._illustrator_name = illustrator_name
        