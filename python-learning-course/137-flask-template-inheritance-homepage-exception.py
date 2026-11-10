# -----------------------------------------------------------------
# Lesson 137: Flask template inheritance -- homepage exception
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : child templates extend base.html, but the
# Topic continuation: homepage renders directly; shared base blocks,
# Topic continuation: a custom child block, and page-specific files
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's key distinction: most pages should have
# their own template and extend a shared base, while the
# homepage is the exception and does not need a child file.
# The shared base supplies the common page structure; child
# pages override a content block. Exact block names in the
# audio are unclear, so this lesson uses "content".
#
# All templates and CSS files are created in a temporary
# project tree, then rendered with Flask's test_client.
# No server is started and no files remain after execution.

import os
import shutil
import tempfile
from flask import Flask, render_template

# ============================================================
# [1] One base, many pages
# ============================================================
# Shared layout belongs in the base; only page-specific
# content belongs in each child template.

print("  base: shared layout for child pages")
#   base: shared layout for child pages
print("  child: page-specific content and title")
#   child: page-specific content and title
print("  homepage: rendered directly, no child template")
#   homepage: rendered directly, no child template

# ============================================================
# [2] Create the project folders
# ============================================================
# Templates live in templates/; CSS assets live in static/.

WORK_DIR = tempfile.mkdtemp(prefix="py137_")
TEMPLATE_DIR = os.path.join(WORK_DIR, "templates")
STATIC_DIR = os.path.join(WORK_DIR, "static")
os.makedirs(TEMPLATE_DIR)
os.makedirs(STATIC_DIR)
print(f"  templates folder exists: {os.path.isdir(TEMPLATE_DIR)}")
#   templates folder exists: True
print(f"  static folder exists: {os.path.isdir(STATIC_DIR)}")
#   static folder exists: True

# ============================================================
# [3] Write base.html
# ============================================================
# The base defines shared document structure and named
# blocks that child pages may override.

base_source = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{% block title %}My Site{% endblock %}</title>
  <link rel="stylesheet" href="/static/main.css">
  <link rel="stylesheet" href="/static/master.css">
</head>
<body>
  <header>Shared Header</header>
  <main>{% block content %}{% endblock %}</main>
  <footer>Shared Footer</footer>
</body>
</html>
"""
base_path = os.path.join(TEMPLATE_DIR, "base.html")
with open(base_path, "w", encoding="utf-8", newline="\n") as page:
    page.write(base_source)
print(f"  base file created: {os.path.isfile(base_path)}")
#   base file created: True

# ============================================================
# [4] Create a child page template
# ============================================================
# About is a child: it extends base.html and fills blocks.

about_source = """{% extends "base.html" %}
{% block title %}About{% endblock %}
{% block content %}<h1>About Page</h1><p>Page-specific text.</p>{% endblock %}
"""
about_path = os.path.join(TEMPLATE_DIR, "about.html")
with open(about_path, "w", encoding="utf-8", newline="\n") as page:
    page.write(about_source)
print(f"  about child file created: {os.path.isfile(about_path)}")
#   about child file created: True
print(f"  about extends base: {'{% extends "base.html" %}' in about_source}")
#   about extends base: True

# ============================================================
# [5] Configure routes
# ============================================================
# The homepage is rendered directly from Python; About
# uses its own child template.

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route("/")
def homepage():
    """Render the homepage directly, without a child file."""
    return "<h1>Homepage</h1><p>Direct homepage response.</p>"

@app.route("/about")
def about():
    """Render the child template that extends the base."""
    return render_template("about.html")

contact_source = """{% extends "base.html" %}
{% block title %}Contact{% endblock %}
{% block content %}<h1>Contact Page</h1>{% endblock %}
"""
contact_path = os.path.join(TEMPLATE_DIR, "contact.html")
with open(contact_path, "w", encoding="utf-8", newline="\n") as page:
    page.write(contact_source)

@app.route("/contact")
def contact():
    return render_template("contact.html")


print(f"  routes: {sorted(rule.rule for rule in app.url_map.iter_rules() if rule.endpoint != 'static')}")
#   routes: ['/', '/about', '/contact']

# ============================================================
# [6] Render the homepage directly
# ============================================================
# No homepage.html is needed for this direct response.

with app.test_client() as client:
    home_response = client.get("/")
home_html = home_response.get_data(as_text=True)
print(f"  homepage status: {home_response.status_code}")
#   homepage status: 200
print(f"  homepage body: {home_html}")
#   homepage body: <h1>Homepage</h1><p>Direct homepage response.</p>
print(f"  homepage template file exists: {os.path.exists(os.path.join(TEMPLATE_DIR, 'home.html'))}")
#   homepage template file exists: False

# ============================================================
# [7] Render About through base.html
# ============================================================
# The child contributes title/content; base contributes
# the shared shell, CSS references, header and footer.

with app.test_client() as client:
    about_response = client.get("/about")
about_html = about_response.get_data(as_text=True)
print(f"  about status: {about_response.status_code}")
#   about status: 200
print(f"  about title: {'<title>About</title>' in about_html}")
#   about title: True
print(f"  about content: {'<h1>About Page</h1>' in about_html}")
#   about content: True
print(f"  shared header: {'<header>Shared Header</header>' in about_html}")
#   shared header: True
print(f"  shared footer: {'<footer>Shared Footer</footer>' in about_html}")
#   shared footer: True

# ============================================================
# [8] Shared blocks can be overridden
# ============================================================
# The title and content blocks are both supplied by About.

print(f"  base has title block: {'{% block title %}' in base_source}")
#   base has title block: True
print(f"  base has content block: {'{% block content %}' in base_source}")
#   base has content block: True
print(f"  base default title replaced: {'<title>My Site</title>' not in about_html}")
#   base default title replaced: True

# ============================================================
# [9] A second child page shares the same base
# ============================================================
# Each non-home page can have its own file while inheriting
# common markup from one base.


# The separate child template and route were registered
# before the first test request, just like About.
print(f"  contact child extends base: {'{% extends "base.html" %}' in contact_source}")
#   contact child extends base: True
print(f"  separate child files: {os.path.basename(about_path)}, {os.path.basename(contact_path)}")
#   separate child files: about.html, contact.html

# ============================================================
# [10] Shared CSS references live in the base
# ============================================================
# Change the shared file once; every child inherits the links.

print(f"  main CSS reference in base: {'/static/main.css' in base_source}")
#   main CSS reference in base: True
print(f"  master CSS reference in base: {'/static/master.css' in base_source}")
#   master CSS reference in base: True
print(f"  both CSS links in About: {'/static/main.css' in about_html and '/static/master.css' in about_html}")
#   both CSS links in About: True

# ============================================================
# [11] Page-specific content versus shared content
# ============================================================
# About has its own body but receives the shared layout.

print(f"  About body is page-specific: {'Page-specific text.' in about_html}")
#   About body is page-specific: True
print(f"  homepage skips shared child shell: {'Shared Header' not in home_html}")
#   homepage skips shared child shell: True
print(f"  About has shared shell: {'Shared Header' in about_html and 'Shared Footer' in about_html}")
#   About has shared shell: True

# ============================================================
# [12] Clean up the temporary project
# ============================================================
# Remove all generated templates and assets.

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# Template architecture inferred from the transcript:
#
#   1. Keep common document structure in base.html
#   2. Child pages extend the base and override named blocks
#   3. Each child page can have its own template file
#   4. The homepage is the exception: it renders directly
#   5. Shared CSS links live once in the base
#   6. A change to the base reaches every child page
#   7. Page-specific body content remains in each child
#   8. Title and content are separate overridable blocks
#   9. Use test_client to verify output without a server
#  10. Temporary template files are removed
#  11. Exact block names in the audio are unclear; this
#      lesson uses title and content as illustrative names
#  12. Do not create a child template for the homepage here
#
# The homepage is deliberately direct; the other pages
# reuse the base and change only their own blocks.
