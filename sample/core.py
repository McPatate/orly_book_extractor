from .extractor import Extractor
from ebooklib import epub

class BookGeneration():
    def __init__(self, book_id):
        # init extraction
        self.extractor = Extractor(book_id)
        self.extractor.sign_in()

        # init epub
        self.book = epub.EpubBook()

    def create_book(self):
        self.book_info = self.extractor.get_book_info()
