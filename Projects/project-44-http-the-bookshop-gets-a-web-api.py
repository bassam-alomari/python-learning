# ============================================================
# Project 44 - http.server: the bookshop gets a web API
# ============================================================
# What this lesson teaches:
#   http.server          a server is a socket with manners
#   BaseHTTPRequestHandler  a handler is a class with do_GET and friends
#   the request line      METHOD path VERSION - just text with a shape
#   status codes          200, 404, 405, 500 - the whole answer
#   JSON over HTTP        the bookshop's data, served as application/json
#   query parameters      the ? part is just more text after the path
#   POST bodies           a POST carries data, and Content-Length says how long
#   http.client           the raw client: you build the request yourself
#   log_message           the server's diary, redirected off stderr
#   shutdown()            stopping serve_forever, and releasing the port
#
# Everything is the standard library. The server binds to port 0, so the
# operating system picks a free port and the output never depends on it.
# The server's log is redirected into a list, so stderr stays empty.
#
# Run it:  python project-44-http-the-bookshop-gets-a-web-api.py
# ============================================================

import http.client
import json
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  which module runs an HTTP server")
print("Q2  what does a request line look like")
print("Q3  what is a 404")
print("Q4  what does the ? in a URL mean")
print("Q5  how does a POST carry data")
print("Q6  what is http.client")
print("Q7  what is a 500")
print("Q8  what does shutdown() do")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  http.server, and a handler is a class with do_GET and friends")
print("Q2  METHOD path VERSION - e.g. GET /books HTTP/1.1")
print("Q3  a status code: the server understood you but has no such page")
print("Q4  query parameters - more text after the path")
print("Q5  in the body, with Content-Length saying how long")
print("Q6  the raw client: you build the request yourself")
print("Q7  a status code: the server broke, and it knows it")
print("Q8  it stops serve_forever, and server_close releases the port")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - a server is a socket with manners")
print("T1  the server answered -> 200")
print("T1  the body -> the bookshop is open")
print("T1  the server is a socket with manners -> True")
print()

print("TASK 2 - the request line")
print("T2  the request line the server saw -> GET /books HTTP/1.1")
print("T2  the client asked for -> /books")
print("T2  so a request is just text with a shape -> True")
print()

print("TASK 3 - status codes")
print("T3  a known path -> 200")
print("T3  an unknown path -> 404")
print("T3  a wrong method -> 405")
print("T3  so the status code is the whole answer -> True")
print()

print("TASK 4 - the bookshop's first endpoint")
print("T4  the shop answered with JSON -> ['Dune', 'Hyperion', 'Foundation', 'Kindred']")
print("T4  the content type -> application/json")
print("T4  so the shop speaks JSON over HTTP -> True")
print()

print("TASK 5 - query parameters")
print("T5  /books?title=Dune -> ['Dune']")
print("T5  /books?title=Nope -> []")
print("T5  so the ? part is just more text -> True")
print()

print("TASK 6 - POST adds a book")
print("T6  POST added a book -> 201")
print("T6  the shop now holds -> ['Dune', 'Hyperion', 'Foundation', 'Kindred', 'The Left Hand of Darkness']")
print("T6  so a POST carries a body, and the server reads it -> True")
print()

print("TASK 7 - http.client, the raw client")
print("T7  the raw client saw -> 200 OK")
print("T7  the content type -> application/json")
print("T7  so urllib and http.client are the same conversation -> True")
print()

print("TASK 8 - errors are just status codes")
print("T8  /boom -> 500")
print("T8  /missing -> 404")
print("T8  so an error is a status code with a body, nothing more -> True")
print()

print("TASK 9 - the server's diary")
print("T9  the server kept a diary of -> 20 requests")
print("T9  the first entry -> \"GET / HTTP/1.1\" 200 -")
print("T9  the query entry -> \"GET /books?title=Dune HTTP/1.1\" 200 -")
print("T9  the last entry -> \"GET /missing HTTP/1.1\" 404 -")
print("T9  an error request logs twice -> True")
print("T9  so every request left a trace -> True")
print()

print("TASK 10 - the loop, closed: shutdown")
print("T10  the server stopped -> True")
print("T10  the port was released -> True")
print("T10  threads still running at the end -> []")
print("T10  every thread was joined or shut down -> True")
print("T10  and the folder this file lives in is untouched -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)

projects_before = sorted(os.listdir(SCRIPT_DIR))

LOG = []
REQUEST = {}
BOOKS = ["Dune", "Hyperion", "Foundation", "Kindred"]


class ShopHandler(BaseHTTPRequestHandler):
    """The bookshop's front door. Each request gets a fresh instance."""

    def _send(self, code, payload, content_type):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        REQUEST["method"] = self.command
        REQUEST["path"] = self.path
        REQUEST["version"] = self.request_version
        REQUEST["line"] = "{0} {1} {2}".format(
            self.command, self.path, self.request_version)
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/books":
            query = urllib.parse.parse_qs(parsed.query)
            title = query.get("title", [None])[0]
            if title is not None:
                payload = json.dumps(
                    [b for b in BOOKS if b == title]).encode()
            else:
                payload = json.dumps(BOOKS).encode()
            self._send(200, payload, "application/json")
        elif parsed.path == "/boom":
            self.send_error(500, "Internal Server Error")
        elif parsed.path == "/":
            self._send(200, b"the bookshop is open", "text/plain")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/books":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode()
            BOOKS.append(json.loads(raw))
            payload = json.dumps(BOOKS).encode()
            self._send(201, payload, "application/json")
        else:
            self.send_error(405)

    def log_message(self, fmt, *args):
        # The default writes to stderr; this file keeps stderr empty and
        # writes the diary into a list instead.
        LOG.append(fmt % args)


server = HTTPServer(("127.0.0.1", 0), ShopHandler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()


def fetch(path, method="GET", data=None):
    """Return just the status code of a request."""
    url = "http://127.0.0.1:{0}{1}".format(port, path)
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as err:
        return err.code


def fetch_body(path):
    """Return the body of a request, even an error page."""
    url = "http://127.0.0.1:{0}{1}".format(port, path)
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode()
    except urllib.error.HTTPError as err:
        return err.read().decode()


# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - a server is a socket with manners")
print("-" * 60)
with urllib.request.urlopen(
        "http://127.0.0.1:{0}/".format(port)) as resp:
    status = resp.status
    body = resp.read().decode()

check("the server answered 200", status == 200)
check("the body is the greeting", body == "the bookshop is open")
check("the server thread is alive", thread.is_alive())
check("the port is a real port", isinstance(port, int) and port > 0)
check("the server is bound to loopback",
      server.server_address[0] == "127.0.0.1")

print("T1  the server answered ->", status)
print("T1  the body ->", body)
print("T1  the server is a socket with manners ->",
      status == 200 and body == "the bookshop is open")
print()

# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - the request line")
print("-" * 60)
with urllib.request.urlopen(
        "http://127.0.0.1:{0}/books".format(port)) as resp:
    resp.read()
line = REQUEST["line"]

check("the request line is GET /books HTTP/1.1",
      line == "GET /books HTTP/1.1")
check("the path is /books", REQUEST["path"] == "/books")
check("the method is GET", REQUEST["method"] == "GET")
check("the version is HTTP/1.1", REQUEST["version"] == "HTTP/1.1")

print("T2  the request line the server saw ->", line)
print("T2  the client asked for ->", REQUEST["path"])
print("T2  so a request is just text with a shape ->",
      line == "GET /books HTTP/1.1")
print()

# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - status codes")
print("-" * 60)
known = fetch("/")
unknown = fetch("/missing")
wrong_method = fetch("/", method="POST")

check("a known path is 200", known == 200)
check("an unknown path is 404", unknown == 404)
check("a wrong method is 405", wrong_method == 405)
check("the three codes are distinct", len({known, unknown, wrong_method}) == 3)
check("the codes are what the server chose",
      known == 200 and unknown == 404 and wrong_method == 405)

print("T3  a known path ->", known)
print("T3  an unknown path ->", unknown)
print("T3  a wrong method ->", wrong_method)
print("T3  so the status code is the whole answer ->",
      known == 200 and unknown == 404 and wrong_method == 405)
print()

# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - the bookshop's first endpoint")
print("-" * 60)
with urllib.request.urlopen(
        "http://127.0.0.1:{0}/books".format(port)) as resp:
    books = json.loads(resp.read().decode())
    ctype = resp.headers.get("Content-Type")

check("the shop answered with four books",
      books == ["Dune", "Hyperion", "Foundation", "Kindred"])
check("the content type is JSON", ctype == "application/json")
check("the body parses as JSON", isinstance(books, list))
check("the first book is Dune", books[0] == "Dune")
check("the list round-trips",
      json.dumps(books) == '["Dune", "Hyperion", "Foundation", "Kindred"]')

print("T4  the shop answered with JSON ->", books)
print("T4  the content type ->", ctype)
print("T4  so the shop speaks JSON over HTTP ->",
      books == ["Dune", "Hyperion", "Foundation", "Kindred"]
      and ctype == "application/json")
print()

# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - query parameters")
print("-" * 60)
with urllib.request.urlopen(
        "http://127.0.0.1:{0}/books?title=Dune".format(port)) as resp:
    found = json.loads(resp.read().decode())
with urllib.request.urlopen(
        "http://127.0.0.1:{0}/books?title=Nope".format(port)) as resp:
    none = json.loads(resp.read().decode())

check("title=Dune matched one book", found == ["Dune"])
check("title=Nope matched nothing", none == [])
check("the query was parsed from the URL",
      found == ["Dune"] and none == [])
check("both answers are JSON lists",
      isinstance(found, list) and isinstance(none, list))
check("the filter is exact, not fuzzy", none == [])

print("T5  /books?title=Dune ->", found)
print("T5  /books?title=Nope ->", none)
print("T5  so the ? part is just more text ->",
      found == ["Dune"] and none == [])
print()

# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - POST adds a book")
print("-" * 60)
data = json.dumps("The Left Hand of Darkness").encode()
req = urllib.request.Request(
    "http://127.0.0.1:{0}/books".format(port), data=data, method="POST")
with urllib.request.urlopen(req) as resp:
    code = resp.status
    after = json.loads(resp.read().decode())
    ctype6 = resp.headers.get("Content-Type")

check("POST answered 201", code == 201)
check("the shop now holds five books", len(after) == 5)
check("the new book is last", after[-1] == "The Left Hand of Darkness")
check("the content type is JSON", ctype6 == "application/json")
check("the body round-trips",
      after == ["Dune", "Hyperion", "Foundation", "Kindred",
                "The Left Hand of Darkness"])

print("T6  POST added a book ->", code)
print("T6  the shop now holds ->", after)
print("T6  so a POST carries a body, and the server reads it ->",
      code == 201 and after[-1] == "The Left Hand of Darkness")
print()

# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - http.client, the raw client")
print("-" * 60)
conn = http.client.HTTPConnection("127.0.0.1", port)
conn.request("GET", "/books")
resp = conn.getresponse()
status7 = resp.status
reason = resp.reason
ctype7 = resp.getheader("Content-Type")
books7 = json.loads(resp.read().decode())
conn.close()

check("the raw client saw 200", status7 == 200)
check("the reason is OK", reason == "OK")
check("the content type is JSON", ctype7 == "application/json")
check("the body parses", isinstance(books7, list))
check("the raw client saw five books", len(books7) == 5)

print("T7  the raw client saw ->", "{0} {1}".format(status7, reason))
print("T7  the content type ->", ctype7)
print("T7  so urllib and http.client are the same conversation ->",
      status7 == 200 and ctype7 == "application/json")
print()

# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - errors are just status codes")
print("-" * 60)
boom = fetch("/boom")
missing = fetch("/missing")
boom_body = fetch_body("/boom")
missing_body = fetch_body("/missing")

check("/boom is a 500", boom == 500)
check("/missing is a 404", missing == 404)
check("the 500 body names the error", "Internal Server Error" in boom_body)
check("the 404 body names the error", "Not Found" in missing_body)
check("the two errors differ", boom != missing)

print("T8  /boom ->", boom)
print("T8  /missing ->", missing)
print("T8  so an error is a status code with a body, nothing more ->",
      boom == 500 and missing == 404)
print()

# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - the server's diary")
print("-" * 60)
# send_error logs twice: once as "code N, message M" (log_error) and once
# as the request line (send_response -> log_request). So an error request
# leaves two entries, and the diary is longer than the request count.
check("the diary has twenty entries", len(LOG) == 20)
check("the first entry is the greeting",
      LOG[0] == '"GET / HTTP/1.1" 200 -')
check("the query entry is the Dune search",
      LOG[8] == '"GET /books?title=Dune HTTP/1.1" 200 -')
check("the last entry is the 404",
      LOG[-1] == '"GET /missing HTTP/1.1" 404 -')
check("an error request logs twice",
      LOG.count("code 500, message Internal Server Error") == 2
      and LOG.count('"GET /boom HTTP/1.1" 500 -') == 2)

print("T9  the server kept a diary of ->", len(LOG), "requests")
print("T9  the first entry ->", LOG[0])
print("T9  the query entry ->", LOG[8])
print("T9  the last entry ->", LOG[-1])
print("T9  an error request logs twice ->",
      LOG.count("code 500, message Internal Server Error") == 2
      and LOG.count('"GET /boom HTTP/1.1" 500 -') == 2)
print("T9  so every request left a trace ->", len(LOG) == 20)
print()

# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the loop, closed: shutdown")
print("-" * 60)
server.shutdown()
server.server_close()
stopped = not thread.is_alive()

probe = None
try:
    probe = http.client.HTTPConnection("127.0.0.1", port)
    probe.request("GET", "/")
    probe.getresponse()
    released = False
except OSError:
    released = True
finally:
    if probe is not None:
        probe.close()

alive = [t.name for t in threading.enumerate()
         if t is not threading.main_thread()]
projects_after = sorted(os.listdir(SCRIPT_DIR))

check("the server stopped", stopped)
check("the port was released", released)
check("no thread was left running", alive == [])
check("the folder this file lives in is untouched",
      projects_before == projects_after)
check("the server thread finished", not thread.is_alive())
check("the diary survived the shutdown", len(LOG) == 20)

print("T10  the server stopped ->", stopped)
print("T10  the port was released ->", released)
print("T10  threads still running at the end ->", alive)
print("T10  every thread was joined or shut down ->", alive == [])
print("T10  and the folder this file lives in is untouched ->",
      projects_before == projects_after)
print()

# ------------------------------------------------------------
# report
# ------------------------------------------------------------
failed = [name for name, ok in CHECKS if not ok]
print("=" * 60)
if failed:
    for name in failed:
        print("  FAILED:", name)
    print("CHECKS PASSED {0} of {1}".format(
        len(CHECKS) - len(failed), len(CHECKS)))
    sys.exit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)