# -----------------------------------------------------------------
# Lesson 135: Flask template inheritance -- base.html
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : a shared base page, Jinja extends/block,
# Example: homepage and about templates, shared CSS links,
# Example: and verifying rendered source with test_client
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript explains why many pages should share a
# base template: update common HTML/CSS once instead of
# editing hundreds or thousands of pages. Each child page
# extends base.html and fills the dynamic body block.
#
# Jinja syntax shown in the lesson:
# Example: {% extends "base.html" %}
# Example: {% block body %}...{% endblock %}
#
# The source video references CSS files that do not exist
# yet, producing 404 requests. This lesson adds the shared
# links to rendered HTML but deliberately does NOT fetch
# absent assets; it reports the source references and the
# 404 behavior as facts instead.

import os
import shutil
import tempfile
from flask import Flask, render_template

# ============================================================
# [1] Why use a base template?
# ============================================================
# Shared document structure belongs in one place.

print("  base template: shared HTML used by child pages")
#   base template: shared HTML used by child pages
print("  shared parts: doctype, head, title, CSS, body shell")
#   shared parts: doctype, head, title, CSS, body shell
print("  child pages: provide only changing body content")
#   child pages: provide only changing body content

# ============================================================
# [2] Create a temporary templates folder
# ============================================================
# Flask convention: templates/ lives beside the app.

WORK_DIR = tempfile.mkdtemp(prefix="py135_")
TEMPLATE_DIR = os.path.join(WORK_DIR, "templates")
os.makedirs(TEMPLATE_DIR)
print(f"  templates folder created: {os.path.isdir(TEMPLATE_DIR)}")
#   templates folder created: True

# ============================================================
# [3] The base template
# ============================================================
# The body block marks the dynamic region. Shared CSS
# references appear once, so future changes are centralized.

base_source = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{% block title %}My Site{% endblock %}</title>
  <link rel="stylesheet" href="/static/css/main.css">
  <link rel="stylesheet" href="/static/css/master.css">
</head>
<body>
  <main>
    {% block body %}{% endblock %}
  </main>
</body>
</html>
"""
base_path = os.path.join(TEMPLATE_DIR, "base.html")
with open(base_path, "w", encoding="utf-8", newline="\n") as page:
    page.write(base_source)
print(f"  base template created: {os.path.basename(base_path)}")
#   base template created: base.html

# ============================================================
# [4] A child page extends base.html
# ============================================================
# Child templates replace only the body block.

home_source = """{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block body %}<h1>Hello From Homepage HTML File</h1>{% endblock %}
"""
about_source = """{% extends "base.html" %}
{% block title %}About{% endblock %}
{% block body %}<h1>Hello From About HTML File</h1>{% endblock %}
"""
for filename, source in (("home.html", home_source), ("about.html", about_source)):
    with open(os.path.join(TEMPLATE_DIR, filename), "w", encoding="utf-8", newline="\n") as page:
        page.write(source)

print(f"  child templates created: {os.path.isfile(os.path.join(TEMPLATE_DIR, 'home.html')) and os.path.isfile(os.path.join(TEMPLATE_DIR, 'about.html'))}")
#   child templates created: True

# ============================================================
# [5] Flask routes render the child templates
# ============================================================
# Set up all routes before the first request.

app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route("/")
def homepage():
    """Render the homepage through its child template."""
    return render_template("home.html")

@app.route("/about")
def about():
    """Render the about page through its child template."""
    return render_template("about.html")

print(f"  routes registered: {sorted(rule.rule for rule in app.url_map.iter_rules() if rule.endpoint != 'static')}")
#   routes registered: ['/', '/about']

# ============================================================
# [6] Homepage output
# ============================================================
# The result contains base markup plus the child's body.

with app.test_client() as client:
    home_response = client.get("/")
home_html = home_response.get_data(as_text=True)
print(f"  homepage status: {home_response.status_code}")
#   homepage status: 200
print(f"  homepage message rendered: {'Hello From Homepage HTML File' in home_html}")
#   homepage message rendered: True
print(f"  homepage title rendered: {'<title>Home</title>' in home_html}")
#   homepage title rendered: True
print(f"  homepage has shared main CSS: {'/static/css/main.css' in home_html}")
#   homepage has shared main CSS: True
print(f"  homepage has shared master CSS: {'/static/css/master.css' in home_html}")
#   homepage has shared master CSS: True

# ============================================================
# [7] About page output
# ============================================================
# A second page changes its body and title, while inheriting
# the same shared document and CSS references.

with app.test_client() as client:
    about_response = client.get("/about")
about_html = about_response.get_data(as_text=True)
print(f"  about status: {about_response.status_code}")
#   about status: 200
print(f"  about message rendered: {'Hello From About HTML File' in about_html}")
#   about message rendered: True
print(f"  about title rendered: {'<title>About</title>' in about_html}")
#   about title rendered: True
print(f"  about has same base CSS: {'/static/css/main.css' in about_html and '/static/css/master.css' in about_html}")
#   about has same base CSS: True

# ============================================================
# [8] Verify inheritance, not duplication
# ============================================================
# The base owns the CSS references; both children extend it.

print(f"  base contains body block: {'{% block body %}' in base_source}")
#   base contains body block: True
print(f"  home extends base: {'{% extends \"base.html\" %}' in home_source}")
#   home extends base: True
print(f"  about extends base: {'{% extends \"base.html\" %}' in about_source}")
#   about extends base: True
print(f"  shared stylesheet reference count: {base_source.count('rel=\"stylesheet\"')}")
#   shared stylesheet reference count: 2

# ============================================================
# [9] One base change reaches both pages
# ============================================================
# Adding one shared stylesheet link changes both rendered
# pages because both inherit the same base template.

print(f"  main CSS appears in both pages: {'/static/css/main.css' in home_html and '/static/css/main.css' in about_html}")
#   main CSS appears in both pages: True
print(f"  master CSS appears in both pages: {'/static/css/master.css' in home_html and '/static/css/master.css' in about_html}")
#   master CSS appears in both pages: True

# ============================================================
# [10] The CSS files are only referenced, not present
# ============================================================
# Like the tutorial at this point, the files have not yet
# been created. Browsers would request them and receive 404.

static_dir = os.path.join(WORK_DIR, "static", "css")
print(f"  CSS assets directory exists: {os.path.isdir(static_dir)}")
#   CSS assets directory exists: False
print("  an absent CSS asset would return: 404 Not Found")
#   an absent CSS asset would return: 404 Not Found

# ============================================================
# [11] The pages share the full document shell
# ============================================================
# The doctype, language, head, and main shell come from base.

print(f"  both pages have one doctype: {home_html.count('<!doctype html>') == 1 and about_html.count('<!doctype html>') == 1}")
#   both pages have one doctype: True
print(f"  both pages have shared main shell: {'<main>' in home_html and '<main>' in about_html}")
#   both pages have shared main shell: True
print(f"  page bodies differ: {'Homepage' in home_html and 'About' in about_html}")
#   page bodies differ: True

# ============================================================
# [12] Clean up the temporary app
# ============================================================
# Remove the temporary templates and files after checking.

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# Template inheritance from the transcript:
#
#   1. Put shared structure in base.html
#   2. Shared structure includes doctype, head, title, CSS
#   3. Put {% block body %}{% endblock %} in the base
#   4. Child pages begin with {% extends "base.html" %}
#   5. Child pages fill the body block with their own HTML
#   6. Homepage and About have different body content
#   7. Both inherit the same title structure and CSS links
#   8. Update a shared CSS link once in the base
#   9. Both rendered pages then contain the new reference
#  10. Missing main.css/master.css requests return 404
#  11. test_client verifies the rendered source without a server
#  12. Temporary templates are removed after the lesson
#
# One base template means one shared change, every child page.
