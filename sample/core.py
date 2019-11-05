from .extractor import Extractor
from ebooklib import epub as ebooklib

class BookGeneration():
    def __init__(self, book_id, user_email, user_password):
        self.id = book_id
        self.extractor = Extractor(book_id, user_email, user_password)
        self.extractor.sign_in()
        self.info = self.extractor.get_book_info()
        self.lang = self.info["language"]
        self.title = self.info["title"]
        self.chapter_spine = []

    def add_authors(self):
        for author in self.info["authors"]:
            self.epub.add_author(author["name"])

    def create_book_style(self):
        style = 'body { font-family: Times, Times New Roman, serif; }'

        nav_css = ebooklib.EpubItem(uid="style_nav",
                                file_name="style/nav.css",
                                media_type="text/css",
                                content=style)
        self.epub.add_item(nav_css)

    def create_images(self):
        print("helo")

    def create_book_chapter(self): # pass info from toc
        # get chapter info
        #   * fetch images
        #   * fetch page assets
        c1 = ebooklib.EpubHtml(title='Introduction',
                        file_name='intro.xhtml',
                        lang=self.lang)
        # get chapter content
        c1.set_content(u'<html><body><h1>Introduction</h1><p>Introduction paragraph.</p></body></html>')
        return c1

    def create_book(self):
        self.epub = ebooklib.EpubBook()
        self.epub.set_identifier(self.id)
        self.epub.set_language(self.lang)
        self.epub.set_title(self.title)
        self.add_authors()
        # get orly toc and loop on each element
        #   create each chapter
        self.epub.toc = ()
        self.epub.spine = self.chapter_spine
        self.epub.add_item(ebooklib.EpubNcx())
        self.epub.add_item(ebooklib.EpubNav())
        ebooklib.write_epub(f"./{self.title}_{self.id}.epub", self.epub)
