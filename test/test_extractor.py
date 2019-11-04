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
        self.__class__.extractor = extractor.Extractor("9781491927274")
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
        self.assertEqual(book_info['url'], "https://learning.oreilly.com/api/v1/book/9781491927274/")