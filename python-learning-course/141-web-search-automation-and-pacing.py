# -----------------------------------------------------------------
# Lesson 141: web automation -- search results and pacing
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : model a search-results workflow, collect links,
# Topic continuation: visit results one at a time, pace actions, and
# Topic continuation: extract fields from each result
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript describes automating a web search: enter
# a query, collect result links, visit each result, read a
# field such as its view count, and pause between pages so
# the workflow does not hammer a website. The exact site and
# selectors are unclear.
#
# Safety and repeatability: this lesson uses local sample
# results, never opens a real website, and injects a fake
# wait callback instead of sleeping. For real automation,
# respect site terms, robots policies, rate limits and APIs.

# ============================================================
# [1] The automation task
# ============================================================
# A workflow can be described without binding to one site.

print("  workflow: search, collect result URLs, visit, extract")
#   workflow: search, collect result URLs, visit, extract
print("  pacing: pause between visits to limit request rate")
#   pacing: pause between visits to limit request rate

# ============================================================
# [2] Sample search results
# ============================================================
# Local fixtures stand in for results returned by a site.

query = "python automation"
search_results = [
    {"title": "Python Guide", "url": "/result/1", "views": 587000},
    {"title": "Web Automation", "url": "/result/2", "views": 42000},
    {"title": "CSS Tutorial", "url": "/result/3", "views": 9100},
]
print(f"  search query: {query}")
#   search query: python automation
print(f"  result count: {len(search_results)}")
#   result count: 3
print(f"  first result title: {search_results[0]['title']}")
#   first result title: Python Guide

# ============================================================
# [3] Collect result URLs
# ============================================================
# In a real browser, these links would be selected from
# the search-results page; here they are fixture data.

result_urls = [result["url"] for result in search_results]
print(f"  collected URLs: {result_urls}")
#   collected URLs: ['/result/1', '/result/2', '/result/3']
print(f"  every result has a URL: {all(result_urls)}")
#   every result has a URL: True

# ============================================================
# [4] Visit results sequentially
# ============================================================
# A simple loop processes one result before the next.

visited = []
for url in result_urls:
    visited.append(url)
print(f"  visited in order: {visited == result_urls}")
#   visited in order: True
print(f"  pages visited: {len(visited)}")
#   pages visited: 3

# ============================================================
# [5] Add a pacing callback
# ============================================================
# Inject wait_fn so tests can record waits without sleeping.

events = []
def fake_wait(seconds):
    """Record a requested pause rather than blocking."""
    events.append(("wait", seconds))

def fake_open(url):
    """Record a local simulated page visit."""
    events.append(("open", url))
    return next(item for item in search_results if item["url"] == url)

def visit_results(urls, open_fn, wait_fn, pause_seconds):
    """Visit links sequentially with a pause between pages."""
    pages = []
    for index, url in enumerate(urls):
        if index:
            wait_fn(pause_seconds)
        pages.append(open_fn(url))
    return pages

pages = visit_results(result_urls, fake_open, fake_wait, 2)
print(f"  pages opened: {sum(event[0] == 'open' for event in events)}")
#   pages opened: 3
print(f"  pauses between pages: {sum(event[0] == 'wait' for event in events)}")
#   pauses between pages: 2
print(f"  each pause is two seconds: {all(value == 2 for kind, value in events if kind == 'wait')}")
#   each pause is two seconds: True

# ============================================================
# [6] Why pause between requests?
# ============================================================
# N pages need N-1 between-page pauses; no need to wait
# before the first visit or after the last one.

print(f"  pause count formula holds: {len(result_urls) - 1 == sum(e[0] == 'wait' for e in events)}")
#   pause count formula holds: True
print(f"  first event is open: {events[0][0] == 'open'}")
#   first event is open: True
print(f"  last event is open: {events[-1][0] == 'open'}")
#   last event is open: True

# ============================================================
# [7] Extract one field from every page
# ============================================================
# The transcript mentions collecting a view count; extract
# the views field from each simulated result.

view_counts = [page["views"] for page in pages]
print(f"  view counts: {view_counts}")
#   view counts: [587000, 42000, 9100]
print(f"  total views: {sum(view_counts)}")
#   total views: 638100
print(f"  highest views: {max(view_counts)}")
#   highest views: 587000

# ============================================================
# [8] Process the last result explicitly
# ============================================================
# A loop handles every element, including the final one.

last_page = pages[-1]
print(f"  final page title: {last_page['title']}")
#   final page title: CSS Tutorial
print(f"  final page views: {last_page['views']}")
#   final page views: 9100
print(f"  final URL visited: {visited[-1]}")
#   final URL visited: /result/3

# ============================================================
# [9] Handle an empty result list
# ============================================================
# No links means no visits and no pauses.

empty_events = []
empty_pages = visit_results([], fake_open, lambda seconds: empty_events.append(seconds), 2)
print(f"  empty search pages: {len(empty_pages)}")
#   empty search pages: 0
print(f"  empty search events: {len(empty_events)}")
#   empty search events: 0

# ============================================================
# [10] Check a configurable delay
# ============================================================
# A caller may choose a slower delay. The lesson records
# the value but deliberately does not sleep.

slow_events = []
def slow_open(url):
    """Record the slower example separately."""
    slow_events.append(("open", url))
    return next(item for item in search_results if item["url"] == url)
def slow_wait(seconds):
    """Record the slower pause separately."""
    slow_events.append(("wait", seconds))
slow_pages = visit_results(result_urls[:2], slow_open, slow_wait, 5)
print(f"  slower pause value: {next(value for kind, value in slow_events if kind == 'wait')}")
#   slower pause value: 5
print(f"  slower example pages: {len(slow_pages)}")
#   slower example pages: 2

# ============================================================
# [11] Keep automation polite and bounded
# ============================================================
# Use official APIs when available, keep request volume low,
# and stop when a page signals blocking or asks you to stop.

print("  real site accessed: False")
#   real site accessed: False
print("  wait callback slept: False")
#   wait callback slept: False
print("  local fixtures used: True")
#   local fixtures used: True

# ============================================================
# [12] Verify event order and clean run state
# ============================================================

open_events = [value for kind, value in events if kind == "open"]
wait_events = [value for kind, value in events if kind == "wait"]
print(f"  open URL order preserved: {open_events == result_urls}")
#   open URL order preserved: True
print(f"  wait events recorded: {len(wait_events)}")
#   wait events recorded: 2
print(f"  final pages match fixtures: {pages == search_results}")
#   final pages match fixtures: True

# ============================================================
# [13] The summary
# ============================================================
# The inferred automation workflow is:
# search for a query; collect result links; visit each link
# in sequence; pause between visits; extract data such as
# views. The site and selectors in the source are unclear,
# so the lesson uses local fixture records and no network.
#
# Prefer an official API and honor site rules/rate limits.
# A pause is a courtesy, not permission to ignore a site's
# access policies.
