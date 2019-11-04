from .extractor import Extractor
from ebooklib import epub

class BookGeneration():
    def __init__(self, book_id, user_email, user_password):
        self.book_id = book_id
        self.extractor = Extractor(book_id, user_email, user_password)
        self.extractor.sign_in()
        self.book_info = self.extractor.get_book_info()
        self.book_lang = self.book_info["language"]
        self.book_title = self.book_info["title"]

    def add_authors(self):
        for author in self.book_info["authors"]:
            self.book.add_author(author["name"])

    def create_book(self):
        self.book = epub.EpubBook()
        self.book.set_identifier(self.book_id)
        self.book.set_language(self.book_lang)
        self.book.set_title(self.book_title)
        self.add_authors()
        # intro chapter
        c1 = epub.EpubHtml(title='Introduction',
                        file_name='intro.xhtml',
                        lang=self.book_lang)
        c1.set_content(u'<html><body><h1>Introduction</h1><p>Introduction paragraph.</p></body></html>')
        c2 = epub.EpubHtml(title='Chapter the Second', file_name='chap02.xhtml', lang='en')
        c2.content = u'<html><head></head><body><h1>Chapter the Second</h1><p>This chapter has two page breaks, both with invisible page numbers.</p>'
        self.book.add_item(c1)
        self.book.add_item(c2)
        style = 'body { font-family: Times, Times New Roman, serif; }'

        nav_css = epub.EpubItem(uid="style_nav",
                                file_name="style/nav.css",
                                media_type="text/css",
                                content=style)
        self.book.add_item(nav_css)
        self.book.toc = ((c1, c2))
        self.book.spine = ['nav', c1, c2]
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        epub.write_epub(f"./{self.book_title}_{self.book_id}.epub", self.book)
