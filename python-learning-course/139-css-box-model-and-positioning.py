# -----------------------------------------------------------------
# Lesson 139: CSS basics -- box sizing and positioning
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : shared CSS files, box-sizing, margin/padding,
# Topic continuation: absolute positioning, percentages and sizing
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript appears to continue the Flask/CSS work:
# shared styling in main.css/master.css, box-sizing,
# margins and padding, then an absolutely positioned
# element sized and placed with percentages. Some spoken
# numbers are unclear; 40px, 15px and 70% are used only as
# illustrative values where the audio suggests them.
#
# CSS is written to temporary files and inspected as text.
# Numeric box-model calculations are explicit, so the lesson
# is deterministic and needs no browser or external package.

import os
import shutil
import tempfile

# ============================================================
# [1] Shared style files
# ============================================================
# Common CSS belongs in a shared stylesheet, not duplicated
# into every page.

print("  main.css and master.css: shared stylesheets")
#   main.css and master.css: shared stylesheets
print("  one shared change can affect every page")
#   one shared change can affect every page

# ============================================================
# [2] Create a temporary static/css folder
# ============================================================
# Match Flask's conventional asset layout.

WORK_DIR = tempfile.mkdtemp(prefix="py139_")
CSS_DIR = os.path.join(WORK_DIR, "static", "css")
os.makedirs(CSS_DIR)
print(f"  CSS folder created: {os.path.isdir(CSS_DIR)}")
#   CSS folder created: True

# ============================================================
# [3] box-sizing: border-box
# ============================================================
# border-box includes padding and border inside the
# declared width/height. This makes sizing predictable.

main_css = """* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
}
"""
main_path = os.path.join(CSS_DIR, "main.css")
with open(main_path, "w", encoding="utf-8", newline="\n") as css_file:
    css_file.write(main_css)

print(f"  universal border-box rule: {'* {' in main_css and 'box-sizing: border-box;' in main_css}")
#   universal border-box rule: True
print(f"  body margin reset: {'margin: 0;' in main_css}")
#   body margin reset: True

# ============================================================
# [4] content-box versus border-box
# ============================================================
# Example: width 200px, horizontal padding 20px each side,
# border 2px each side. content-box adds them outside width.

width = 200
padding_each_side = 20
border_each_side = 2
content_box_outer = width + 2 * padding_each_side + 2 * border_each_side
border_box_outer = width
print(f"  content-box outer width: {content_box_outer}px")
#   content-box outer width: 244px
print(f"  border-box outer width: {border_box_outer}px")
#   border-box outer width: 200px
print(f"  border-box includes padding and border: {border_box_outer == width}")
#   border-box includes padding and border: True

# ============================================================
# [5] Margin versus padding
# ============================================================
# Margin is outside the border; padding is inside it.

spacing_css = """.card {
  margin: 20px;
  padding: 15px;
}
"""
print(f"  margin is outside: {'margin: 20px;' in spacing_css}")
#   margin is outside: True
print(f"  padding is inside: {'padding: 15px;' in spacing_css}")
#   padding is inside: True
print(f"  sample padding: {15}px")
#   sample padding: 15px

# ============================================================
# [6] Center content with text-align
# ============================================================
# text-align centers inline content inside a block.

center_css = ".title { text-align: center; }\n"
print(f"  centered text rule: {'text-align: center;' in center_css}")
#   centered text rule: True

# ============================================================
# [7] Absolute positioning
# ============================================================
# position:absolute removes an element from normal flow.
# Its nearest positioned ancestor becomes the reference.

position_css = """.container {
  position: relative;
}

.badge {
  position: absolute;
  top: 0;
  left: 0;
}
"""
print(f"  relative parent: {'position: relative;' in position_css}")
#   relative parent: True
print(f"  absolute child: {'position: absolute;' in position_css}")
#   absolute child: True
print(f"  top and left offsets: {'top: 0;' in position_css and 'left: 0;' in position_css}")
#   top and left offsets: True

# ============================================================
# [8] Percentage width and height
# ============================================================
# Percentages are relative to the containing block's size.

parent_width = 1000
parent_height = 600
child_width_percent = 70
child_height_percent = 100
child_width = parent_width * child_width_percent / 100
child_height = parent_height * child_height_percent / 100
print(f"  width at 70% of 1000px: {child_width:g}px")
#   width at 70% of 1000px: 700px
print(f"  height at 100% of 600px: {child_height:g}px")
#   height at 100% of 600px: 600px

# ============================================================
# [9] Place an element from all four sides
# ============================================================
# top/right/bottom/left set the edges of an absolutely
# positioned element; width/height:100% fills its parent.

fill_css = """.overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
"""
print(f"  all four offsets present: {all(f'{side}: 0;' in fill_css for side in ('top', 'right', 'bottom', 'left'))}")
#   all four offsets present: True
print(f"  full-size dimensions: {'width: 100%;' in fill_css and 'height: 100%;' in fill_css}")
#   full-size dimensions: True

# ============================================================
# [10] Add a second shared stylesheet
# ============================================================
# Keep site-wide typography/color rules in master.css.

master_css = """body {
  color: #777;
  background: #fff;
}
"""
master_path = os.path.join(CSS_DIR, "master.css")
with open(master_path, "w", encoding="utf-8", newline="\n") as css_file:
    css_file.write(master_css)
print(f"  main stylesheet exists: {os.path.isfile(main_path)}")
#   main stylesheet exists: True
print(f"  master stylesheet exists: {os.path.isfile(master_path)}")
#   master stylesheet exists: True
print(f"  example gray color: {'#777' in master_css}")
#   example gray color: True

# ============================================================
# [11] CSS source is separate from HTML
# ============================================================
# The HTML links to assets; the CSS files own presentation.

html_source = '<link rel="stylesheet" href="main.css">'
print(f"  HTML references stylesheet: {'main.css' in html_source}")
#   HTML references stylesheet: True
print(f"  CSS contains layout rule: {'position: absolute;' in position_css}")
#   CSS contains layout rule: True

# ============================================================
# [12] Inspect the files and clean up
# ============================================================
# Verify both CSS files exist, then remove the sandbox.

print(f"  CSS files created: {len([main_path, master_path])}")
#   CSS files created: 2
shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   sandbox removed: True

# ============================================================
# [13] The summary
# ============================================================
# CSS concepts inferred from this noisy transcript:
#
# Summary: 1. Put shared rules in main.css/master.css
# Summary: 2. box-sizing:border-box includes padding/border in size
# Summary: 3. margin is outside; padding is inside the border
# Summary: 4. text-align:center centers inline content
# Summary: 5. position:absolute uses a positioned ancestor
# Summary: 6. top/right/bottom/left control offsets
# Summary: 7. Percentage sizes are relative to the containing block
# Summary: 8. width/height:100% fill the containing block
# Summary: 9. One shared stylesheet update reaches every page
# Summary: 10. CSS is separate from the HTML document
# Summary: 11. The exact spoken dimensions were unclear; values here
#      are explicit examples, not claimed verbatim
# Summary: 12. Temporary CSS files are removed after the lesson
#
# box sizing controls the edges; positioning controls where
# the box sits; percentages measure it against its parent.
