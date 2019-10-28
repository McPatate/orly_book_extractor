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

    def __init__(self):
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

    def http_req(self, url, method, json=None, perform_redirect=True):
        res = getattr(requests, method)(
                url,
                headers=self.get_headers(),
                json=json,
                allow_redirects=False,
            )
        self.set_cookies(res.cookies)
        self.set_header("cookie", self.get_cookies())
        self.set_header("referer", res.request.url)
        if res.is_redirect and perform_redirect:
            return self.http_req(res.next.url, method, json, perform_redirect)
        return res

    def sign_in(self):
        print("logging in")
        res = self.http_req(self.LOGIN_ENTRY_URL, "get")
        if res == 0:
            print("entr url req failed")
        redirect_uri = res.request.path_url[res.request.path_url.index("redirect_uri"):]
        redirect_uri = redirect_uri[:redirect_uri.index("&")]
        redirect_uri = "https://api.oreilly.com%2Fapi%2Fv1%2Fauth%2Fopenid%2Fauthorize%3F" + redirect_uri

        res = self.http_req(
            self.LOGIN_URL,
            "post",
            json={
                "email": "luc.georges@zenika.com",
                "password": "cJx6ffWpUetu5Zt",
                "redirect_uri": redirect_uri
            },
            perform_redirect=False
        )
        if res == 0 or res.status_code != 200:
            print(res.headers)
            print("login url req failed")
        self.jwt = res.json()
        res = self.http_req(self.jwt["redirect_uri"], "get")
        if res == 0:
            print("jwt redirect req failed")

    def get_book_info(self, id):
        print("infos !")

    def get_book_chapters(self, id):
        print("book chapters!")