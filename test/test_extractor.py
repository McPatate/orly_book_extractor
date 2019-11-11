import os
import unittest
from sample import extractor

class TestCookie():
    def __init__(self, name, value):
        self.name = name
        self.value = value

class TestHttpReq(unittest.TestCase):
    ClassIsSetup = False

    def setUp(self):
        if not self.ClassIsSetup:
            print("Initializing testing environment")
            self.setupClass()
            self.__class__.ClassIsSetup = True
                                
    def setupClass(self):
        unittest.TestCase.setUp(self)
        self.__class__.extractor = extractor.Extractor("9781491927274", os.environ['EMAIL'], os.environ['PSWD'])
        self.extractor.sign_in()

    def test_setting_cookies(self):
        cookies = [TestCookie("cookie1", "value1"), TestCookie("cookie2", "value2")]
        self.extractor.set_cookies(cookies)
        self.assertIn("cookie1=value1; cookie2=value2;", self.extractor.get_cookies())

    def test_setting_header(self):
        self.extractor.set_header("origin", "https://www.google.com")
        self.assertEqual(self.extractor.get_headers()['origin'], "https://www.google.com")

    def test_http_req(self):
        res = self.extractor.http_req('https://www.google.com', "get")
        self.assertEqual(res.status_code, 200)

    def test_sign_in(self):
        self.assertIsNot(self.extractor.jwt, {})

    def test_get_book_info(self):
        book_info = self.extractor.get_book_info()
        self.assertEqual(book_info["url"], "https://learning.oreilly.com/api/v1/book/9781491927274/")

    def test_get_chapter_info(self):
        chapter_info = self.extractor.get_chapter_info("https://learning.oreilly.com/api/v1/book/9781491927274/chapter/ch06.html")
        self.assertEqual(chapter_info["content"], "https://learning.oreilly.com/api/v1/book/9781491927274/chapter-content/ch06.html")

    def test_get_chapter_content(self):
        chapter_content = self.extractor.get_chapter_content("https://learning.oreilly.com/api/v1/book/9781491927274/chapter-content/ch06.html")
        self.assertIn('<section data-type="chapter" epub:type="chapter" data-pdf-bookmark="Chapter 6. Expressions">', chapter_content)

    def test_get_chapter_style(self):
        chapter_style = self.extractor.get_chapter_style("https://learning.oreilly.com/library/css/programming-rust/9781491927274/epub.css")
        self.assertIn('@charset "utf-8";#sbo-rt-content html', chapter_style)

    def test_get_chapter_image(self):
        chapter_image = self.extractor.get_chapter_image("https://learning.oreilly.com/library/view/programming-rust/9781491927274/assets/cover.png")
        with open("test/test.png", "rb") as fd:
            test_img = fd.read()
        self.assertEqual(chapter_image, test_img)

    def test_get_toc(self):
        toc = self.extractor.get_toc()
        self.assertEqual(toc[0]["fragment"], "preface")