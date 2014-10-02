import sys
import requests

NO_ERROR = True
ERRORS = []

# Standard Test
res = requests.get("http://localhost:8080/")
if not res.status_code == 200:
    NO_ERROR = False
    ERRORS.append("standard")

# Redirect Test
res = requests.get("http://localhost:8080/redirect", allow_redirects=False)
if not res.status_code == 303:
    NO_ERROR = False
    ERRORS.append("redirect")

# Environment Test
res = requests.get("http://localhost:8080/env")
if not res.headers.get("Content-Type") == "text/plain;charset=utf-8":
    NO_ERROR = False
    ERRORS.append("env-content")
if not res.headers.get("X-Powered-By") == "ObjectWeb/2.0":
    NO_ERROR = False
    ERRORS.append("env-powered")

# Cookie Handling Test
res = requests.get("http://localhost:8080/cookie")
if not res.cookies.get("CookieName", "") == "CookieValue":
    NO_ERROR = False
    ERRORS.append("cookie-get")

res = requests.post("http://localhost:8080/cookie",
                    cookies={"CookieName": "CookieValue"})
if not res.status_code == 200:
    NO_ERROR = False
    ERRORS.append("cookie-return")

if NO_ERROR:
    print 0, ", ".join(ERRORS)
    sys.exit(0)
else:
    print 1, ", ".join(ERRORS)
    sys.exit(1)
