# -----------------------------------------------------------------
# Lesson 133: Flask -- a tiny web app and its routes
# Course   : Python Programming (Elzero-Style Arabic Course)
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript is noisy, but it clearly points to a
# small Python web framework (likely Flask): install the
# package, create an app, define URL paths/routes, return
# responses, and distinguish development from production.
# Exact route names are unclear, so / and /hello are
# illustrative examples.
#
# Setup and local development commands:
# Production should use a production WSGI server. Never
# expose Flask's interactive debugger to the public.
#
# Flask is installed for this lesson. Flask's test_client
# makes in-process requests without a live server, socket,
# or external network.

import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Define ALL routes before the first test-client request.
@app.route("/")
def home():
    """Return the home page response."""
    return "Home page"

@app.route("/hello")
def hello():
    """Return a short greeting response."""
    return "Hello from the web app"

@app.route("/greet")
def greet():
    """Return a greeting using an optional query value."""
    name = request.args.get("name", "guest")
    return f"Hello, {name}!"

@app.route("/api/status")
def api_status():
    """Return structured data as JSON."""
    return jsonify({"message": "hello", "count": 2})

# ============================================================
# [1] Web app and route concepts
# ============================================================
# A framework connects URL paths to Python functions.

print("  web app: URL paths connected to Python functions")
#   web app: URL paths connected to Python functions
print("  route: a URL path and the code that handles it")
#   route: a URL path and the code that handles it

# ============================================================
# [2] Package installation
# ============================================================
# Flask is an external package; pip installs it.

print("  Flask installed: True")
#   Flask installed: True
print("  install command: python -m pip install flask")
#   install command: python -m pip install flask

# ============================================================
# [3] Register application routes
# ============================================================
# Route paths are explicit URL patterns.

route_paths = sorted(
    rule.rule for rule in app.url_map.iter_rules()
    if rule.endpoint != "static"
)
print(f"  route paths: {route_paths}")
#   route paths: ['/', '/api/status', '/greet', '/hello']

# ============================================================
# [4] Request a page
# ============================================================
# The test client exercises the app without app.run().

with app.test_client() as client:
    home_response = client.get("/")
    hello_response = client.get("/hello")
    missing_response = client.get("/missing")

print(f"  home status: {home_response.status_code}")
#   home status: 200
print(f"  home body: {home_response.get_data(as_text=True)}")
#   home body: Home page
print(f"  hello status: {hello_response.status_code}")
#   hello status: 200
print(f"  hello body: {hello_response.get_data(as_text=True)}")
#   hello body: Hello from the web app
print(f"  unknown route status: {missing_response.status_code}")
#   unknown route status: 404

# ============================================================
# [5] Query parameters
# ============================================================
# request.args reads values after ? in the URL.

with app.test_client() as client:
    greet_response = client.get("/greet?name=Ali")
    default_response = client.get("/greet")

print(f"  query greeting: {greet_response.get_data(as_text=True)}")
#   query greeting: Hello, Ali!
print(f"  default greeting: {default_response.get_data(as_text=True)}")
#   default greeting: Hello, guest!

# ============================================================
# [6] Development and production
# ============================================================
# Debug is useful locally; it should be disabled publicly.

environments = {"development": True, "production": False}
print(f"  development debug: {environments['development']}")
#   development debug: True
print(f"  production debug: {environments['production']}")
#   production debug: False

# ============================================================
# [7] Return a JSON response
# ============================================================
# jsonify produces JSON plus its HTTP content type.

with app.test_client() as client:
    json_response = client.get("/api/status")
json_data = json_response.get_json()
print(f"  JSON body: {json.dumps(json_data, sort_keys=True)}")
#   JSON body: {"count": 2, "message": "hello"}
print(f"  JSON content type: {json_response.mimetype}")
#   JSON content type: application/json

# ============================================================
# [8] Verify the route behavior
# ============================================================
# Turn expectations into executable checks.

checks = [
    home_response.status_code == 200,
    hello_response.status_code == 200,
    missing_response.status_code == 404,
    greet_response.get_data(as_text=True) == "Hello, Ali!",
    json_data == {"message": "hello", "count": 2},
]
print(f"  route checks: {len(checks)}")
#   route checks: 5
print(f"  every route check passes: {all(checks)}")
#   every route check passes: True

# ============================================================
# [9] Keep business logic reusable
# ============================================================
# Route code can call a plain, independently testable function.

def make_greeting(name):
    """Build a greeting string."""
    return f"Hello, {name}!"

print(f"  reusable function: {make_greeting('Mona')}")
#   reusable function: Hello, Mona!
print(f"  function independently testable: {make_greeting('Ali') == 'Hello, Ali!'}")
#   function independently testable: True

# ============================================================
# [10] Development server command
# ============================================================
# Document the command, but do not start a long-running server.

print("  development command: flask --app app run --debug")
#   development command: flask --app app run --debug
print("  this lesson starts no server: True")
#   this lesson starts no server: True

# ============================================================
# [11] WSGI
# ============================================================
# WSGI connects Python web applications to web servers.

print("  WSGI: interface between Python apps and web servers")
#   WSGI: interface between Python apps and web servers
print(f"  Flask WSGI callable: {callable(app.wsgi_app)}")
#   Flask WSGI callable: True

# ============================================================
# [12] Final local request
# ============================================================
# One last in-process request; no socket is opened.

with app.test_client() as client:
    final_response = client.get("/")
print(f"  final request: {final_response.status_code} {final_response.get_data(as_text=True)}")
#   final request: 200 Home page
print(f"  in-process request succeeded: {final_response.status_code == 200}")
#   in-process request succeeded: True

# ============================================================
# [13] The summary
# ============================================================
# Flask basics inferred from the unclear transcript:
# install with pip; create an app; map URL routes to views;
# return text or JSON; read query arguments; use debug only
# in development; test with Flask test_client; deploy with
# a production WSGI server. Exact route names in the audio
# are unclear, so the paths above are illustrative.

# A route is a small contract: URL path in, response out.
