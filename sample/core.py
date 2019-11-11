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

    def create_images(self, images, base_img_url):
        for image in images:
            img_type = image.split(".")[-1]
            if img_type == "jpg":
                img_type = "jpeg"
            img_content = self.extractor.get_chapter_image(f"{base_img_url}{image}")
            epub_img = ebooklib.EpubItem(file_name=image, media_type=f"image/{img_type}", content=img_content)
            self.epub.add_item(epub_img)

    # TODO
    #   parse html and change links to :
    #     * assets
    #     * other pages
    def create_book_chapter(self, chapter_url):
        chapter_info = self.extractor.get_chapter_info(chapter_url)
        chapter_content = self.extractor.get_chapter_content(chapter_info["content"])
        if chapter_info != None and chapter_content != None:
            title = chapter_info["title"]
            print(f"create_book_chapter: creating {title}")
            chapter = ebooklib.EpubHtml(title=title,
                            file_name=chapter_info["full_path"].replace("html", "xhtml"),
                            lang=self.lang)
            chapter.set_content(chapter_content)
            for stylesheet in chapter_info["stylesheets"]:
                css_url = stylesheet["url"]
                name = stylesheet["full_path"]
                if css_url not in self.styles:
                    style = self.extractor.get_chapter_style(css_url)
                    nav_css = ebooklib.EpubItem(uid=f"style_{name.replace('.css', '')}",
                                            file_name=f"{name}",
                                            media_type="text/css",
                                            content=style)
                    self.styles.append(css_url)
                    chapter.add_item(nav_css)
            self.chapters.append(chapter)
            self.epub.add_item(chapter)
            self.create_images(chapter_info["images"], chapter_info["asset_base_url"])
        else:
            print("create_book_chapter: errored on ", chapter_url)

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
