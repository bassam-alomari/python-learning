# Python Learning Progress — Bassam Alomari

Started: 15/8/2026 (returning to programming after forgetting)

## Current Level
- Beginner — **Switched courses on 16/8**: Dropped Elzero (felt he wasn't explaining well) → A slower, more detailed second course (folder `second-course\main.py` — covers print, variables, types, operations, %, input, str())

## Golden Rules
- Learning via YouTube (Arabic Python course) + **Immediate practice**: Write along with the video in a code file
- Every time you finish a segment/lesson → Write a small summary in a practice file (I help you)
- Mistakes are not bad — you learn from them (and they are documented here!)

## Common Mistakes (Error Log)
| Date | Mistake | Fix |
|---|---|---|
| 15/8/2026 | `=` instead of `==` in comparison | Use `==` for comparison, `=` for assignment |
| 15/8/2026 | Forgetting `:` after `if` | Every condition must end with `:` |
| 15/8/2026 | Array index: `sum[2]` on a 2-element array | Indexing starts at 0, last index = count - 1 |
| 15/8/2026 | Accumulator variable without initial value (`x=x+prices[i]`) | `x = 0` before the loop |
| 15/8/2026 | `range(1,5)` instead of `range(0,4)` | Loop starts at 0 to capture the first element |
| 15/8/2026 | Writing `dist` instead of `dict` in a comment | The correct type for a dictionary is `dict` |
| 16/8/2026 | `int = 1` then `int(input(...))` → `TypeError: 'int' object is not callable` | **Never name a variable with a built-in function name** (`int`/`float`/`str`/`print`...) — it hijacks the name from Python. Fix: `my_int`/`num`... |
| 16/8/2026 | `float = 1.1` in the same file — time bomb | Fixed for the same reason (`my_float`) |

## Completed Lessons
- [x] Lessons 2-8 (15/8): Printing + Comments + Data Types + Variables — Inline files (1-Print.py / 2-comments.py / 3-Data_Types.py / 4-Variables_Part1.py) ✅
  - Note: The user writes exercises **inside the lesson files** (inline system) — this is his style, we respect it
- [ ] Lessons 9-12 (practice): Escape Sequences + Concatenation + String Methods + Slicing — Challenge: Slicing exercises (can be in an existing file)

## Current Practice Tasks
- [ ] Lesson 12: File `5-Slicing.py` (slicing challenge)
- [ ] Lesson 4: (done) File `4-Variables.py` — old challenge finished in Variables_Part1
- [ ] DSA path: Two Sum (NeetCode) — first question, after mastering lists + loops + dictionaries (~end of week 1)

## Progress (Updated Each Session)
- 15/8/2026: Started warm-up, wrote first real code (loop + array + if) — minor errors being fixed
- 15/8/2026: Switched to Elzero course — completed first 12 lessons (print, comments, data types, variables, slicing...) ✅ — Rating: Excellent, with note: practical file per lesson coming
- 16/8/2026: Switched to second course (slower, clearer) — Wrote complete `main.py` (9 sections: print, variables, types, operations, %, input) — **Diagnosed and analyzed `int = 1` error together** ✅ | ✅ Fix successful, file runs to the end (40 = 20 + 20)
- 16/8/2026: **🏆 First 100% independent program: Calculator App** — input + float + 5 operations, ran first try with all correct results — better than the video host's solution (which was broken) ✅ — Rating: 10/10
- 16/8/2026: **🌍 Project on the internet:** `python-learning` repo public on GitHub (`bassam-alomari`) — Files organized (elzero-course / second-course) and pushed successfully ✅ — First published project on the profile
- 16/8/2026: **👑 First "smart" program: Advanced_Calculator_App.py** — Applied if/elif/else to the calculator: operator selection + **divide-by-zero protection** + "Bad Operator" message — Successful on first run with three test cases (normal / zero division / invalid operator) — Self-taught: comparisons + logical operators + conditions (sections 11-15 in main.py) — Rating: 10/10
