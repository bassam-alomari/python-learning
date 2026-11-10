# -----------------------------------------------------------------
# Lesson 136: Flask static files -- static_folder and url_for
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : the static/ directory, CSS and image assets,
# Topic continuation: url_for('static', filename=...), verifying
# Topic continuation: paths and the 404 response for missing files
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# This continues the Flask templates sequence. The audio
# mentions missing main.css and master.css files, checking
# whether they exist, and seeing 404 Not Found when a
# referenced asset is absent. Flask serves CSS, images and
# other fixed assets from a static/ folder by default.
#
# The examples use a temporary project tree. Existing
# assets are requested with Flask test_client; a missing
# asset is checked as a 404 response. No server is started.

import os
import shutil
import tempfile
from flask import Flask, url_for

# ============================================================
# [1] Static files are not templates
# ============================================================
# Templates are rendered; static assets are served unchanged.

print("  templates: rendered HTML pages")
#   templates: rendered HTML pages
print("  static: CSS, images and other fixed files")
#   static: CSS, images and other fixed files

# ============================================================
# [2] Flask's default static directory
# ============================================================
# Flask convention: a static/ folder sits beside the app.

WORK_DIR = tempfile.mkdtemp(prefix="py136_")
STATIC_DIR = os.path.join(WORK_DIR, "static")
CSS_DIR = os.path.join(STATIC_DIR, "css")
os.makedirs(CSS_DIR)

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")
print(f"  static folder configured: {os.path.isdir(STATIC_DIR)}")
#   static folder configured: True
print(f"  Flask static URL path: {app.static_url_path}")
#   Flask static URL path: /static

# ============================================================
# [3] Create stylesheet assets
# ============================================================
# The tutorial references main.css and master.css. Create
# both files so requests return 200 instead of 404.

main_path = os.path.join(CSS_DIR, "main.css")
master_path = os.path.join(CSS_DIR, "master.css")
with open(main_path, "w", encoding="utf-8", newline="\n") as css_file:
    css_file.write("body { color: navy; }\n")
with open(master_path, "w", encoding="utf-8", newline="\n") as css_file:
    css_file.write("h1 { font-weight: bold; }\n")

print(f"  main.css exists: {os.path.isfile(main_path)}")
#   main.css exists: True
print(f"  master.css exists: {os.path.isfile(master_path)}")
#   master.css exists: True

# ============================================================
# [4] Build URLs with url_for
# ============================================================
# Avoid hard-coding /static/... when Flask can generate
# the correct URL from an endpoint and filename.

with app.test_request_context():
    main_url = url_for("static", filename="css/main.css")
    master_url = url_for("static", filename="css/master.css")

print(f"  main URL: {main_url}")
#   main URL: /static/css/main.css
print(f"  master URL: {master_url}")
#   master URL: /static/css/master.css
print(f"  URLs start at static endpoint: {main_url.startswith('/static/') and master_url.startswith('/static/')}")
#   URLs start at static endpoint: True

# ============================================================
# [5] Request each existing asset
# ============================================================
# test_client asks Flask for the files without a running
# development server or open network port.

with app.test_client() as client:
    main_response = client.get(main_url)
    main_body = main_response.get_data(as_text=True).strip()
    main_response.close()
    master_response = client.get(master_url)
    master_body = master_response.get_data(as_text=True).strip()
    master_response.close()

print(f"  main.css status: {main_response.status_code}")
#   main.css status: 200
print(f"  main.css content type: {main_response.mimetype}")
#   main.css content type: text/css
print(f"  main.css body: {main_body}")
#   main.css body: body { color: navy; }
print(f"  master.css status: {master_response.status_code}")
#   master.css status: 200
print(f"  master.css body: {master_body}")
#   master.css body: h1 { font-weight: bold; }

# ============================================================
# [6] The missing-file 404
# ============================================================
# Referencing a filename does not create the file. If it
# is absent from static/, Flask responds 404 Not Found.

missing_path = os.path.join(CSS_DIR, "missing.css")
with app.test_request_context():
    missing_url = url_for("static", filename="css/missing.css")
with app.test_client() as client:
    missing_response = client.get(missing_url)
    missing_status = missing_response.status_code
    missing_response.close()

print(f"  missing.css exists: {os.path.exists(missing_path)}")
#   missing.css exists: False
#   missing.css status: 404
print(f"  missing.css status: {missing_status}")
# Summary: missing.css is not found: True

# ============================================================
# [7] Filesystem path versus URL path
# ============================================================
# A disk path locates the file locally; a URL is what a
# browser requests. They are related, but not the same.

print(f"  disk basename: {os.path.basename(main_path)}")
#   disk basename: main.css
print(f"  disk file exists: {os.path.isfile(main_path)}")
#   disk file exists: True
print(f"  URL is different from disk path: {main_url != main_path}")
#   URL is different from disk path: True

# ============================================================
# [8] Generate the link used in HTML
# ============================================================
# A template can call url_for('static', filename=...).

html_link = f'<link rel="stylesheet" href="{main_url}">'
print(f"  generated stylesheet link: {html_link}")
#   generated stylesheet link: <link rel="stylesheet" href="/static/css/main.css">
print(f"  link points to the requested file: {main_url.endswith('main.css')}")
#   link points to the requested file: True

# ============================================================
# [9] Static assets use ordinary subfolders
# ============================================================
# Organize images, CSS and JavaScript under static/.

images_dir = os.path.join(STATIC_DIR, "images")
os.makedirs(images_dir)
logo_path = os.path.join(images_dir, "logo.txt")
with open(logo_path, "w", encoding="utf-8", newline="\n") as logo_file:
    logo_file.write("demo logo")
with app.test_request_context():
    logo_url = url_for("static", filename="images/logo.txt")
with app.test_client() as client:
    logo_response = client.get(logo_url)
    logo_status = logo_response.status_code
    logo_body = logo_response.get_data(as_text=True)
    logo_response.close()

print(f"  nested asset URL: {logo_url}")
#   nested asset URL: /static/images/logo.txt
print(f"  nested asset status: {logo_status}")
#   nested asset status: 200
print(f"  nested asset body: {logo_body}")
#   nested asset body: demo logo

# ============================================================
# [10] A shared base can reference shared assets
# ============================================================
# One generated URL can be used in every page's base template.

shared_links = [main_url, master_url]
print(f"  shared stylesheet count: {len(shared_links)}")
#   shared stylesheet count: 2
print(f"  all shared assets exist: {main_response.status_code == 200 and master_response.status_code == 200}")
#   all shared assets exist: True

# ============================================================
# [11] Missing assets explain browser 404s
# ============================================================
# A broken link appears in the browser's network panel as
# a client-side 404; a filename in HTML alone is not enough.

print("  absent referenced asset: 404 Not Found")
#   absent referenced asset: 404 Not Found
print(f"  missing URL contains missing.css: {'missing.css' in missing_url}")
#   missing URL contains missing.css: True

# ============================================================
# [12] Verify and clean the sandbox
# ============================================================
# All generated files are temporary and removed at the end.

print(f"  assets created: {len([main_path, master_path, logo_path])}")
#   assets created: 3
shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# Static file handling in Flask:
#
# Summary: 1. Use static/ for CSS, images and other fixed files
# Summary: 2. Keep rendered HTML templates in templates/
# Summary: 3. url_for("static", filename="css/main.css") builds a URL
# Summary: 4. The disk path and browser URL are different concepts
# Summary: 5. Existing main.css and master.css return status 200
# Summary: 6. A URL to a file that is not present returns 404
# Summary: 7. Organize assets into static/css and static/images
# Summary: 8. Use generated static URLs in a shared base template
# Summary: 9. test_client verifies assets without starting a server
# Summary: 10. The transcript's missing CSS files explain its 404
# Summary: 11. Create the file before expecting a successful request
# Summary: 12. Temporary project files are cleaned up
#
# Flask serves a static URL only when its corresponding
# file exists under the configured static folder.
