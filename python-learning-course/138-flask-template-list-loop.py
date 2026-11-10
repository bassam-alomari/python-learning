# -----------------------------------------------------------------
# Lesson 138: Flask -- pass a list to a template and loop
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : send a Python list from a route to a new
# Topic continuation: template, iterate over its items with Jinja,
# Topic continuation: display indexes and verify rendered HTML
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript appears to revisit rendering a page from
# data: create a new page/template, pass it a list (likely
# records with names and values), then use a template loop
# to display each entry. The exact data fields and page name
# are unclear, so this lesson uses a small language list.
#
# Flask's test_client runs the route in-process; no server
# or network is started. All generated templates live in a
# temporary directory and are removed at the end.

import os
import shutil
import tempfile
from flask import Flask, render_template

# ============================================================
# [1] Prepare a list in Python
# ============================================================
# The route will pass this collection into the page.

languages = ["Python", "JavaScript", "SQL", "HTML", "CSS"]
print(f"  list length: {len(languages)}")
#   list length: 5
print(f"  first item: {languages[0]}")
#   first item: Python

# ============================================================
# [2] Create the templates directory
# ============================================================
# Flask looks for templates in the configured folder.

WORK_DIR = tempfile.mkdtemp(prefix="py138_")
TEMPLATE_DIR = os.path.join(WORK_DIR, "templates")
os.makedirs(TEMPLATE_DIR)
print(f"  templates folder exists: {os.path.isdir(TEMPLATE_DIR)}")
#   templates folder exists: True

# ============================================================
# [3] Write a template with a for loop
# ============================================================
# Jinja loops over a list passed by the route.

page_source = """<!doctype html>
<title>Languages</title>
<h1>Languages</h1>
<ul>
{% for language in languages %}
  <li>{{ loop.index }}. {{ language }}</li>
{% endfor %}
</ul>
"""
page_path = os.path.join(TEMPLATE_DIR, "languages.html")
with open(page_path, "w", encoding="utf-8", newline="\n") as page_file:
    page_file.write(page_source)
print(f"  template created: {os.path.basename(page_path)}")
#   template created: languages.html
print(f"  template has Jinja for: {'{% for language in languages %}' in page_source}")
#   template has Jinja for: True

# ============================================================
# [4] Pass the list from a route
# ============================================================
# render_template sends keyword values to the Jinja context.

app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route("/languages")
def languages_page():
    """Render the language list page."""
    return render_template("languages.html", languages=languages)

print(f"  route registered: {'/languages' in [rule.rule for rule in app.url_map.iter_rules()]}")
#   route registered: True

# ============================================================
# [5] Render the list page
# ============================================================
# Request the route with Flask's in-process test client.

with app.test_client() as client:
    response = client.get("/languages")
html = response.get_data(as_text=True)
print(f"  response status: {response.status_code}")
#   response status: 200
print(f"  page title rendered: {'<title>Languages</title>' in html}")
#   page title rendered: True

# ============================================================
# [6] Each list item becomes an HTML row
# ============================================================
# Jinja executes the loop and substitutes each value.

print(f"  Python rendered: {'<li>1. Python</li>' in html}")
#   Python rendered: True
print(f"  CSS rendered: {'<li>5. CSS</li>' in html}")
#   CSS rendered: True
print(f"  every language appears: {all(language in html for language in languages)}")
#   every language appears: True
print(f"  rendered list item count: {html.count('<li>')}")
#   rendered list item count: 5

# ============================================================
# [7] Jinja loop indexes
# ============================================================
# loop.index starts at 1; loop.index0 starts at 0.

index_source = """{% for language in languages %}{{ loop.index0 }}={{ language }};{% endfor %}"""
from jinja2 import Environment
index_text = Environment(autoescape=True).from_string(index_source).render(languages=languages)
print(f"  zero-based loop indexes: {index_text}")
#   zero-based loop indexes: 0=Python;1=JavaScript;2=SQL;3=HTML;4=CSS;
print(f"  indexes cover every list item: {index_text.count('=') == len(languages)}")
#   indexes cover every list item: True

# ============================================================
# [8] Empty list behavior
# ============================================================
# A loop may have no rows; Jinja also supports an else clause.

empty_source = """{% for item in items %}{{ item }}{% else %}No items{% endfor %}"""
empty_text = Environment(autoescape=True).from_string(empty_source).render(items=[])
print(f"  empty-list message: {empty_text}")
#   empty-list message: No items

# ============================================================
# [9] Pass records, not only strings
# ============================================================
# A list of dictionaries can expose multiple fields per row.

courses = [
    {"name": "Python", "level": "beginner"},
    {"name": "Flask", "level": "web"},
]
record_source = """{% for course in courses %}<li>{{ course.name }}: {{ course.level }}</li>{% endfor %}"""
record_html = Environment(autoescape=True).from_string(record_source).render(courses=courses)
print(f"  record rows rendered: {record_html.count('<li>')}")
#   record rows rendered: 2
print(f"  Flask record rendered: {'Flask: web' in record_html}")
#   Flask record rendered: True

# ============================================================
# [10] Escaping still applies inside a loop
# ============================================================
# Untrusted values are escaped by default.

unsafe_names = ["<script>", "Safe"]
escaped_html = Environment(autoescape=True).from_string(
    "{% for name in names %}<li>{{ name }}</li>{% endfor %}"
).render(names=unsafe_names)
print(f"  unsafe list value escaped: {'&lt;script&gt;' in escaped_html}")
#   unsafe list value escaped: True
print(f"  literal script tag absent: {'<li><script></li>' not in escaped_html}")
#   literal script tag absent: True

# ============================================================
# [11] Verify route data and template separation
# ============================================================
# Python owns the data; the template owns repeated markup.

print(f"  list stays in Python: {languages == ['Python', 'JavaScript', 'SQL', 'HTML', 'CSS']}")
#   list stays in Python: True
print(f"  loop stays in template: {'{% for language in languages %}' in page_source}")
#   loop stays in template: True
print(f"  source file exists: {os.path.isfile(page_path)}")
#   source file exists: True

# ============================================================
# [12] Clean up the temporary page
# ============================================================
# Remove the generated project tree after testing.

shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# Passing a list into a Flask/Jinja page:
#
#   1. Keep data in a Python list
#   2. Pass it by name to render_template(...)
#   3. Use {% for value in values %} in the template
#   4. Jinja repeats the HTML for each element
#   5. loop.index starts at 1; loop.index0 starts at 0
#   6. Use an {% else %} block for an empty collection
#   7. Lists of dictionaries can expose several fields
#   8. Jinja autoescapes unsafe values in HTML templates
#   9. Flask test_client checks the rendered page locally
#  10. Keep data preparation in Python and presentation in HTML
#  11. The transcript's exact list/page fields are unclear;
#      the language list is an illustrative example
#  12. Temporary templates are removed after testing
#
# Python supplies the collection; the template decides how
# every element becomes a visible row.
