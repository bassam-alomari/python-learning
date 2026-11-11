# -----------------------------------------------------------------
# Lesson 140: CSS animations -- keyframes and transitions
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : a shared stylesheet, @keyframes, animation
# Topic continuation: duration, from/to percentages, moving and
# Topic continuation: fading elements, and applying rules to a group
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript appears to continue the shared CSS work
# and introduce a simple animation. The legible cues include
# CSS files linked from the shared base, an element starting
# at one position/opacity and moving toward a target, plus
# applying a rule to multiple elements. Exact values are
# unclear; 0-to-80px, 0.7 opacity and 2s are examples.
#
# This lesson writes CSS to a temporary file and verifies
# key declarations as text. Actual animation rendering is
# browser behavior; no browser is launched here.

import os
import shutil
import tempfile

# ============================================================
# [1] Animation lives in shared CSS
# ============================================================
# Put repeated animation rules in the shared stylesheet.

print("  animation: a CSS property changes over time")
print("  shared stylesheet: one rule can affect many elements")

# ============================================================
# [2] Create the shared CSS folder
# ============================================================
# Match the static/css structure from earlier lessons.

WORK_DIR = tempfile.mkdtemp(prefix="py140_")
CSS_DIR = os.path.join(WORK_DIR, "static", "css")
os.makedirs(CSS_DIR)
css_path = os.path.join(CSS_DIR, "master.css")
print(f"  CSS folder created: {os.path.isdir(CSS_DIR)}")

# ============================================================
# [3] Define keyframes
# ============================================================
# @keyframes names the animation and describes its states.

animation_css = """@keyframes slide-in {
  from {
    transform: translateX(0);
    opacity: 0;
  }
  to {
    transform: translateX(80px);
    opacity: 0.7;
  }
}

.animated-item {
  animation: slide-in 2s ease-in-out;
}
"""
with open(css_path, "w", encoding="utf-8", newline="\n") as css_file:
    css_file.write(animation_css)

print(f"  keyframes declared: {'@keyframes slide-in' in animation_css}")
print(f"  start state present: {'translateX(0)' in animation_css and 'opacity: 0;' in animation_css}")
print(f"  target state present: {'translateX(80px)' in animation_css and 'opacity: 0.7;' in animation_css}")

# ============================================================
# [4] Set a duration and timing function
# ============================================================
# The duration controls how long the animation takes.

print(f"  duration set to two seconds: {'2s' in animation_css}")
print(f"  easing function: {'ease-in-out' in animation_css}")

# ============================================================
# [5] Apply the animation to one element
# ============================================================
# The class connects a DOM element to the keyframes.

print(f"  class rule exists: {'.animated-item {' in animation_css}")
print(f"  class uses animation name: {'animation: slide-in' in animation_css}")

# ============================================================
# [6] Apply the rule to several elements
# ============================================================
# A shared selector can target every matching element.

multiple_css = animation_css + "\n.card, .badge, .notice { animation: slide-in 2s ease-in-out; }\n"
print(f"  group selector targets three classes: {'.card, .badge, .notice' in multiple_css}")
print(f"  group receives same animation: {'animation: slide-in 2s ease-in-out' in multiple_css}")

# ============================================================
# [7] Animation shorthand parts
# ============================================================
# animation-name, duration and timing function can also
# be declared separately.

separate_css = """.notice {
  animation-name: slide-in;
  animation-duration: 2s;
  animation-timing-function: ease-in-out;
}
"""
print(f"  separate name property: {'animation-name: slide-in;' in separate_css}")
print(f"  separate duration property: {'animation-duration: 2s;' in separate_css}")
print(f"  shorthand and longhand name agree: {'slide-in' in animation_css and 'slide-in' in separate_css}")

# ============================================================
# [8] Use percentages for intermediate states
# ============================================================
# Keyframes can describe intermediate points too.

three_step_css = """@keyframes fade-and-move {
  0% { opacity: 0; transform: translateX(0); }
  50% { opacity: 1; transform: translateX(40px); }
  100% { opacity: 0.7; transform: translateX(80px); }
}
"""
print(f"  0 percent state: {'0%' in three_step_css}")
print(f"  50 percent state: {'50%' in three_step_css}")
print(f"  100 percent state: {'100%' in three_step_css}")

# ============================================================
# [9] Animation versus transition
# ============================================================
# A transition usually responds to a property change;
# keyframes can define a multi-step sequence.

transition_css = ".button { transition: opacity 0.3s ease; }\n"
print(f"  transition declaration available: {'transition:' in transition_css}")
print(f"  keyframes allow multiple stages: {'50%' in three_step_css and '100%' in three_step_css}")

# ============================================================
# [10] Inspect the shared file
# ============================================================
# Verify the CSS was written exactly where intended.

with open(css_path, "r", encoding="utf-8") as css_file:
    saved_css = css_file.read()
print(f"  saved file basename: {os.path.basename(css_path)}")
print(f"  saved CSS matches source: {saved_css == animation_css}")

# ============================================================
# [11] Animation settings as explicit values
# ============================================================
# Keep the example's start, target and duration together.

settings = {"start_x": 0, "end_x": 80, "start_opacity": 0, "end_opacity": 0.7, "duration_seconds": 2}
print(f"  moves right: {settings['end_x'] > settings['start_x']}")
print(f"  fades in: {settings['end_opacity'] > settings['start_opacity']}")
print(f"  duration positive: {settings['duration_seconds'] > 0}")

# ============================================================
# [12] Clean up the temporary stylesheet
# ============================================================
# Remove the sandbox after inspection.

print(f"  CSS file exists: {os.path.isfile(css_path)}")
shutil.rmtree(WORK_DIR, ignore_errors=True)
print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")

# ============================================================


#     animation: a CSS property changes over time
#     shared stylesheet: one rule can affect many elements
#     CSS folder created: True
#     keyframes declared: True
#     start state present: True
#     target state present: True
#     duration set to two seconds: True
#     easing function: True
#     class rule exists: True
#     class uses animation name: True
#     group selector targets three classes: True
#     group receives same animation: True
#     separate name property: True
#     separate duration property: True
#     shorthand and longhand name agree: True
#     0 percent state: True
#     50 percent state: True
#     100 percent state: True
#     transition declaration available: True
#     keyframes allow multiple stages: True
#     saved file basename: master.css
#     saved CSS matches source: True
#     moves right: True
#     fades in: True
#     duration positive: True
#     CSS file exists: True
#     sandbox removed: True

# [13] The summary
# ============================================================
# ============================================================
# CSS animation ideas: shared stylesheet, @keyframes, from/to or percentage states, duration and easing, selectors for multiple elements, and transitions. Values are illustrative; no browser is launched, and temporary files are cleaned up.
#
# Keyframes define what changes; the animation rule defines
# how long and how smoothly the browser moves between states.
