from .extractor import Extractor
from ebooklib import epub as ebooklib
import json

class BookGeneration():
    def __init__(self, book_id, user_email, user_password):
        self.id = book_id
        self.extractor = Extractor(book_id, user_email, user_password)
        self.extractor.sign_in()
        self.info = self.extractor.get_book_info()
        self.lang = self.info["language"]
        self.title = self.info["title"]
        self.chapters = []
        self.styles = []

    def add_authors(self):
        for author in self.info["authors"]:
            self.epub.add_author(author["name"])

    def create_book_style(self, css_url):
        if css_url not in self.styles:
            style = self.extractor.get_chapter_style(css_url)
            nav_css = ebooklib.EpubItem(uid="style_nav",
                                    file_name="style/nav.css",
                                    media_type="text/css",
                                    content=style)
            self.epub.add_item(nav_css)
            self.styles.append(css_url)

    def create_images(self):
        print("helo")

    # TODO
    #   parse html and change links to :
    #     * assets
    #     * imgs
    #   get :
    #     * fetch images
    #     * fetch page assets
    def create_book_chapter(self, chapter_url): # pass info from toc
        chapter_info = self.extractor.get_chapter_info(chapter_url)
        chapter_content = self.extractor.get_chapter_content(chapter_info["content"])
        if chapter_info != None and chapter_content != None:
            chapter = ebooklib.EpubHtml(title=chapter_info["title"],
                            file_name=chapter_info["full_path"].replace("html", "xhtml"),
                            lang=self.lang)
            chapter.set_content(chapter_content)
            self.chapters.append(chapter)
            self.epub.add_item(chapter)
        else:
            print("create_book_chapter: errored on ", chapter_url)

    def create_toc(self):
        toc = self.extractor.get_toc()
        self.epub.toc = (toc)

    def create_book(self):
        self.epub = ebooklib.EpubBook()
        self.epub.set_identifier(self.id)
        self.epub.set_language(self.lang)
        self.epub.set_title(self.title)
        self.add_authors()
        for chapter_url in self.info["chapters"]:
            self.create_book_chapter(chapter_url)
        self.epub.spine = self.chapters
        self.epub.add_item(ebooklib.EpubNcx())
        self.epub.add_item(ebooklib.EpubNav())
        ebooklib.write_epub(f"./{self.title}.epub", self.epub)
