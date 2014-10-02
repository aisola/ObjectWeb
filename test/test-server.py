import sys

sys.path.insert(0, '..')

import ObjectWeb


class MainPage(object):
    def GET(self):
        ObjectWeb.status("200 OK")
        return "PASS"

    def POST(self):
        ObjectWeb.status("200 OK")
        return "REDIRECT PASS"


class RedirectHandler(object):
    def GET(self):
        ObjectWeb.seeother("/")


class EnvHandler(object):
    def GET(self):
        ObjectWeb.header("Content-Type", "text/plain")
        ObjectWeb.header("X-Powered-By", "ObjectWeb/2.0")
        return str(ObjectWeb.context)


class CookieRelay(object):
    def GET(self):
        ObjectWeb.status("200 OK")
        ObjectWeb.setcookie("CookieName", "CookieValue")
        return ""

    def POST(self):
        cookies = ObjectWeb.cookies()
        if not cookies:
            ObjectWeb.status("404 Not Found")
            return ""
        else:
            ObjectWeb.status("200 OK")
            return cookies.get("CookieName", "")


app = ObjectWeb.Application({
    "/": MainPage,
    "/redirect": RedirectHandler,
    "/env": EnvHandler,
    "/cookie": CookieRelay,
}).run(port=8080)
