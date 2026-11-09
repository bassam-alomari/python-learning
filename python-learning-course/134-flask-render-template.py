# -----------------------------------------------------------------
# Lesson 134: Flask templates -- render_template and HTML pages
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : render HTML templates, pass route data, test responses
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript continues the Flask topic from lesson 133.
# The clearest cues are "render", a page file, its path,
# and building a page whose content can be controlled from
# the route. This lesson demonstrates Flask's
# render_template() with a templates/ folder and variables.
# Exact page name and route in the audio are unclear, so
# /profile and profile.html are illustrative.
#
# Flask convention: project/app.py plus project/templates/profile.html
#
# Here, the same structure is created in a temporary
# directory so no extra lesson files remain in the repo.

import os
import shutil
import tempfile
from flask import Flask, render_template

# ============================================================
# [1] A template is a separate page file
# ============================================================
# Keep HTML out of a long Python string in the route.

print("  template: an HTML page stored separately")
#   template: an HTML page stored separately
print("  Flask default folder: templates")
#   Flask default folder: templates

# ============================================================
# [2] Create the conventional folder structure
# ============================================================
# Flask looks for templates/ next to the application.

WORK_DIR = tempfile.mkdtemp(prefix="py134_")
template_dir = os.path.join(WORK_DIR, "templates")
os.makedirs(template_dir)
print(f"  templates folder created: {os.path.isdir(template_dir)}")
#   templates folder created: True

# ============================================================
# [3] Write a simple HTML template
# ============================================================
# Jinja placeholders use {{ variable }} syntax.

template_path = os.path.join(template_dir, "profile.html")
template_source = """<!doctype html>
<title>Profile</title>
<h1>Hello, {{ name }}!</h1>
<p>Role: {{ role }}</p>
"""
with open(template_path, "w", encoding="utf-8", newline="\n") as page_file:
    page_file.write(template_source)
print(f"  template file created: {os.path.basename(template_path)}")
#   template file created: profile.html

# ============================================================
# [4] Configure Flask to find the template
# ============================================================
# template_folder may be supplied when making the app.

list_path = os.path.join(template_dir, "items.html")
list_source = """<ul>
{% for item in items %}
<li>{{ item }}</li>
{% endfor %}
</ul>
"""
with open(list_path, "w", encoding="utf-8", newline="\n") as page_file:
    page_file.write(list_source)


app = Flask(__name__, template_folder=template_dir)
print(f"  Flask app created: {app.name.endswith('133-flask-web-app-routes') is False}")
#   Flask app created: True
print(f"  template folder configured: {app.jinja_loader is not None}")
#   template folder configured: True

# ============================================================
# [5] Render the template from a route
# ============================================================
# render_template finds the file by name and fills values.

@app.route("/profile")
def profile():
    """Render a profile page using the template file."""
    return render_template("profile.html", name="Ali", role="Student")

@app.route("/profile/<name>")
def named_profile(name):
    """Render the profile with a name from the URL."""
    return render_template("profile.html", name=name, role="Visitor")


@app.route("/items")
def items_page():
    """Render a list of items."""
    return render_template("items.html", items=["book", "lamp"])


print(f"  route registered: {'/profile' in [rule.rule for rule in app.url_map.iter_rules()]}")
#   route registered: True

# ============================================================
# [6] Request and render the page
# ============================================================
# Flask's test client runs the route without a server.

with app.test_client() as client:
    response = client.get("/profile")

html = response.get_data(as_text=True)
print(f"  response status: {response.status_code}")
#   response status: 200
print(f"  content type: {response.mimetype}")
#   content type: text/html
print(f"  title rendered: {'<title>Profile</title>' in html}")
#   title rendered: True

# ============================================================
# [7] Template variables become page content
# ============================================================
# Values passed by the route replace the placeholders.

print(f"  name rendered: {'<h1>Hello, Ali!</h1>' in html}")
#   name rendered: True
print(f"  role rendered: {'<p>Role: Student</p>' in html}")
#   role rendered: True
print(f"  placeholders remain: {'{{ name }}' in html or '{{ role }}' in html}")
#   placeholders remain: False

# ============================================================
# [8] Change page content with route data
# ============================================================
# The same template can render different values.


with app.test_client() as client:
    other_response = client.get("/profile/Mona")
other_html = other_response.get_data(as_text=True)
print(f"  dynamic route status: {other_response.status_code}")
#   dynamic route status: 200
print(f"  dynamic name rendered: {'<h1>Hello, Mona!</h1>' in other_html}")
#   dynamic name rendered: True
print(f"  dynamic role rendered: {'<p>Role: Visitor</p>' in other_html}")
#   dynamic role rendered: True

# ============================================================
# [9] Jinja escapes unsafe HTML by default
# ============================================================
# Do not mark untrusted strings safe; escaped output
# prevents user text becoming active markup.

with app.test_client() as client:
    unsafe_response = client.get("/profile/<script>")
unsafe_html = unsafe_response.get_data(as_text=True)
print(f"  unsafe text escaped: {'&lt;script&gt;' in unsafe_html}")
#   unsafe text escaped: True
print(f"  unsafe script not emitted as tag: {'<h1>Hello, <script>' not in unsafe_html}")
#   unsafe script not emitted as tag: True

# ============================================================
# [10] A template can contain a loop
# ============================================================
# HTML structure can repeat data supplied by Python.



with app.test_client() as client:
    items_response = client.get("/items")
items_html = items_response.get_data(as_text=True)
print(f"  item list status: {items_response.status_code}")
#   item list status: 200
print(f"  both list items rendered: {'<li>book</li>' in items_html and '<li>lamp</li>' in items_html}")
#   both list items rendered: True

# ============================================================
# [11] The rendered page is a normal response
# ============================================================
# A rendered template can be inspected with standard
# response properties, just like other Flask responses.

print(f"  rendered page status is successful: {response.status_code == 200}")
#   rendered page status is successful: True

# ============================================================
# [12] Template safety and cleanup
# ============================================================
# Close the client's resources and remove every temporary
# file after the example is complete.

print(f"  profile file exists: {os.path.isfile(template_path)}")
#   profile file exists: True
print(f"  template source has placeholder: {'{{ name }}' in template_source}")
#   template source has placeholder: True
shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# Flask template ideas inferred from the transcript:
#
#   1. Put HTML files in templates/
#   2. Flask(__name__) creates the application
#   3. render_template("profile.html", ...) loads a page
#   4. Pass values from a route to template placeholders
#   5. One template can render different values
#   6. Jinja loops repeat HTML for collections
#   7. Jinja escapes unsafe text by default
#   8. Test rendering with Flask's test_client
#   9. Keep templates separate from Python route logic
#  10. Jinja escapes unsafe text by default
#  11. The audio's exact filenames and routes are unclear;
#  12. Temporary files are removed after the demonstration
#
# A route supplies data; a template shapes it into a page.
