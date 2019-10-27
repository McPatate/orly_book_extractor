import unittest
from sample import extractor

class Cookie():
    def __init__(self, name, value):
        self.name = name
        self.value = value

class TestHttpReq(unittest.TestCase):
    def setUp(self):
        self.extractor = extractor.Extractor()

    def test_setting_cookies(self):
        cookies = [Cookie("cookie1", "value1"), Cookie("cookie2", "value2")]
        self.extractor.set_cookies(cookies)
        self.assertEqual(self.extractor.get_cookies(), "cookie1=value1; cookie2=value2;")

    def test_setting_header(self):
        self.extractor.set_header("origin", "https://www.google.com")
        self.assertEqual(self.extractor.get_headers(), {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate",
            "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "cookie": "",
            "pragma": "no-cache",
            "origin": "https://www.google.com",
            "referer": "https://learning.oreilly.com/login/unified/?next=/home/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/60.0.3112.113 Safari/537.36",
        })

    def test_http_req(self):
        res = self.extractor.http_req('https://www.google.com', "get")
        self.assertEqual(res.status_code, 200)
