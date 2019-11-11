import requests
import json

class Extractor():
    ORLY_BASE_HOST = "oreilly.com"

    SAFARI_BASE_HOST = "learning." + ORLY_BASE_HOST
    API_ORIGIN_HOST = "api." + ORLY_BASE_HOST

    ORLY_BASE_URL = "https://www." + ORLY_BASE_HOST
    SAFARI_BASE_URL = "https://" + SAFARI_BASE_HOST
    API_ORIGIN_URL = "https://" + API_ORIGIN_HOST

    LOGIN_URL = ORLY_BASE_URL + "/member/auth/login/"
    LOGIN_ENTRY_URL = SAFARI_BASE_URL + "/login/unified/?next=/home/"

    BOOK_URL = SAFARI_BASE_URL + "/api/v1/book/{0}/"

    def __init__(self, book_id, user_email, user_password):
        self.jwt = {}
        self.cookies = {}
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate",
            "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "cookie": "",
            "pragma": "no-cache",
            "origin": self.SAFARI_BASE_URL,
            "referer": self.LOGIN_ENTRY_URL,
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/60.0.3112.113 Safari/537.36",
        }
        self.book_id = book_id
        self.BOOK_URL = self.BOOK_URL.format(self.book_id)
        self.user_email = user_email
        self.user_password = user_password

    def set_cookies(self, jar):
        for cookie in jar:
            if cookie.name != "sessionid": # wut ?
                self.cookies.update({
                    cookie.name: cookie.value
                })

    def set_header(self, name, value):
        self.headers.update({
            name: value
        })

    def get_cookies(self):
        return " ".join(["{0}={1};".format(k, v) for k, v in self.cookies.items()])

    def get_headers(self):
        return self.headers

    def http_req(self, url, method, json=None, perform_redirect=True, stream=False):
        res = getattr(requests, method)(
                url,
                headers=self.get_headers(),
                json=json,
                allow_redirects=False,
                stream=stream
            )
        try:
            self.set_cookies(res.cookies)
            self.set_header("cookie", self.get_cookies())
            self.set_header("referer", res.request.url)
            if res.is_redirect and perform_redirect:
                return self.http_req(res.next.url, method, json, perform_redirect)
        except:
            print(f"http_req: error requesting {url}")
            return None
        return res

    def sign_in(self):
        print("sign_in: logging in")
        res = self.http_req(self.LOGIN_ENTRY_URL, "get")
        if res == 0:
            print("sign_in: entry url req failed")
        redirect_uri = res.request.path_url[res.request.path_url.index("redirect_uri"):]
        redirect_uri = redirect_uri[:redirect_uri.index("&")]
        redirect_uri = "https://api.oreilly.com%2Fapi%2Fv1%2Fauth%2Fopenid%2Fauthorize%3F" + redirect_uri

        res = self.http_req(
            self.LOGIN_URL,
            "post",
            json={
                "email": self.user_email,
                "password": self.user_password,
                "redirect_uri": redirect_uri
            },
            perform_redirect=False
        )
        if res == 0 or res.status_code != 200:
            print(res.headers)
            print("sign_in: login url req failed")
        self.jwt = res.json()
        res = self.http_req(self.jwt["redirect_uri"], "get")
        if res == 0:
            print("sign_in: jwt redirect req failed")
        print("sign_in: login successful")

    def get_book_info(self):
        res = self.http_req(self.BOOK_URL, "get")
        if res == 0:
            print("get_book_info: book info req failed")
        try:
            res = res.json()
        except ValueError:
            print("get_book_info: invalid json")
            return None
        return res

    def get_chapter_info(self, url):
        res = self.http_req(url, "get")
        if res == 0:
            print("get_chapter_info: chapter info req failed")
        try:
            res = res.json()
        except ValueError:
            print("get_chapter_info: invalid json")
            return None
        return res

    def get_chapter_content(self, content_url):
        res = self.http_req(content_url, "get")
        if res == 0:
            print("get_chapter_content: chapter content req failed")
        try:
            res = res.text
        except ValueError:
            print("get_chapter_content: invalid response")
            return None
        return res

    def get_chapter_style(self, url):
        res = self.http_req(url, "get")
        if res == 0:
            print("get_chapter_info: style req failed")
        try:
            res = res.text
        except ValueError:
            print("get_chapter_style: invalid response")
            return None
        return res

    def get_chapter_image(self, url):
        res = self.http_req(url, "get", stream=True)
        if res == 0:
            print("get_chapter_image: image req failed")
        try:
            res = res.raw.read()
        except ValueError:
            print("get_chapter_image: invalid response")
            return None
        return res

    def get_toc(self):
        res = self.http_req(f"{self.BOOK_URL}toc", "get")
        if res == 0:
            print("get_toc: toc req failed")
        try:
            res = res.json()
        except ValueError:
            print("get_toc: invalid json")
            return None
        return res
