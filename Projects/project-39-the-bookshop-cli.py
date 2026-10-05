# ============================================================
# PROJECT 39 - THE BOOKSHOP CLI
# ============================================================
#
# Project 38 gave you a shop you could run. This one lets other people
# *drive* it, from a terminal, with words instead of Python.
#
# And it keeps the one rule this course has never broken: there is no
# input() and no keyboard anywhere. That is not stubbornness, it is the
# whole point of this project:
#
#     argv is just a list of strings.
#
# So your command line program is not something you have to poke by
# hand to test. main(["add-book", "Dune", "Herbert", "--copies", "3"])
# is an ordinary function call with an ordinary list argument. You can
# assert on its return value, capture its output, and know the answer
# will be identical on every machine, forever.
#
# Run it:  python project-39-the-bookshop-cli.py
# Run the session:  python project-39-the-bookshop-cli.py report
# ============================================================

import argparse
import contextlib
import csv
import io
import json
import os
import sys
import tempfile
import unittest

# Exit codes are a public contract. A shell, a Makefile and a CI
# pipeline all read them, and none of them read your error message.
OK = 0        # it worked
REFUSED = 1   # your program understood the command and said no
USAGE = 2     # argparse did not understand the command at all


class CliError(Exception):
    """Anything the user should be told about, politely."""


# ============================================================
# THE SHOP - the same ideas as project 38, kept small
# ============================================================

class Catalogue:
    def __init__(self):
        self.books = {}

    def add(self, title, author, copies):
        title = str(title).strip()
        author = str(author).strip()
        if not title or not author:
            raise CliError("a book needs both a title and an author")
        if title in self.books:
            raise CliError("already in stock: " + title)
        number = to_int(copies)
        if number is None:
            raise CliError("copies must be a whole number")
        if number < 0:
            raise CliError("copies must not be negative")
        self.books[title] = {"title": title, "author": author, "copies": number}

    def titles(self):
        return sorted(self.books)

    def size(self):
        return len(self.books)

    def rows(self):
        return [self.books[title] for title in self.titles()]

    def load_rows(self, rows):
        self.books = {}
        for row in rows:
            self.add(row.get("title"), row.get("author"), row.get("copies", 0))


def to_int(value, default=None):
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return default
    return default


class Shop:
    def __init__(self):
        self.catalogue = Catalogue()
        self.members = []
        self.loans = {}
        self.fines = []
        self.loan_days = 14
        self.fine_per_day = 2

    def add_member(self, name):
        name = str(name).strip()
        if not name:
            raise CliError("a member needs a name")
        if name in self.members:
            raise CliError("already a member: " + name)
        self.members.append(name)

    def borrow(self, member, title, day):
        if member not in self.members:
            raise CliError("not a member: " + str(member))
        if title not in self.catalogue.books:
            raise CliError("not in stock: " + str(title))
        if (member, title) in self.loans:
            raise CliError("already borrowed: " + title)
        self.loans[(member, title)] = to_int(day, 0) + self.loan_days

    def give_back(self, member, title, day):
        due = self.loans.pop((member, title), None)
        if due is None:
            raise CliError("not on loan: " + str(title))
        fine = max(0, to_int(day, 0) - due) * self.fine_per_day
        self.fines.append({"member": member, "title": title, "fine": fine})
        return fine

    def open_loans(self):
        return len(self.loans)

    def report(self):
        if self.catalogue.size() == 0 and not self.members:
            return ["nothing to report"]
        lines = ["books " + str(self.catalogue.size()) +
                 "  members " + str(len(self.members)) +
                 "  open loans " + str(self.open_loans())]
        for title in self.catalogue.titles():
            lines.append("  " + title + " by " + self.catalogue.books[title]["author"])
        for member, title in sorted(self.loans):
            lines.append("  on loan: " + member + " has " + title +
                         " (due day " + str(self.loans[(member, title)]) + ")")
        return lines

    def to_dict(self):
        return {
            "books": self.catalogue.rows(),
            "fines": [dict(fine) for fine in self.fines],
            "loans": [{"member": member, "title": title, "due": due}
                      for (member, title), due in sorted(self.loans.items())],
            "members": sorted(self.members),
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise CliError("the state file must hold an object")
        shop = cls()
        shop.catalogue.load_rows(data.get("books", []))
        for name in data.get("members", []):
            if name not in shop.members:
                shop.members.append(name)
        shop.loans = {}
        for record in data.get("loans", []):
            key = (record.get("member"), record.get("title"))
            if None not in key:
                shop.loans[key] = to_int(record.get("due"), 0)
        shop.fines = [dict(fine) for fine in data.get("fines", [])]
        return shop


# ============================================================
# THE STATE FILE
# ============================================================

def dumps_canonical(data):
    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def save_state(path, shop):
    folder = os.path.dirname(os.path.abspath(path))
    handle, temporary = tempfile.mkstemp(dir=folder, suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(dumps_canonical(shop.to_dict()))
        os.replace(temporary, path)
    except BaseException:
        if os.path.exists(temporary):
            os.unlink(temporary)
        raise


def load_state(path):
    if not os.path.exists(path):
        return Shop()
    with open(path, "r", encoding="utf-8") as stream:
        return Shop.from_dict(json.load(stream))


def export_csv(path, rows):
    """lineterminator has to be given, or Windows writes \\r\\n and the
    same catalogue becomes two different files on two different systems."""
    with open(path, "w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["title", "author", "copies"],
                                lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def import_csv(path):
    if not os.path.exists(path):
        raise CliError("no such file: " + path)
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            rows.append({"title": (row.get("title") or "").strip(),
                         "author": (row.get("author") or "").strip(),
                         "copies": to_int(row.get("copies"), 0)})
    return rows


# ============================================================
# THE PARSER
# ============================================================
#
# Three details here are not decoration, and task 8 pays for all three.
#
# 1. parents=[common]. A shared flag has to be repeated on every
#    subcommand, otherwise bookshop borrow Sara Dune --state x.json is
#    rejected as an argument 'borrow' never had.
#
# 2. default=argparse.SUPPRESS on that shared copy. This is the one
#    that bites. If the shared copy carries a normal default, then a
#    --state given BEFORE the subcommand is parsed correctly by the
#    main parser and then silently overwritten by the subparser's
#    default. Exit code 0, no warning, and your shop saved to the
#    wrong file. SUPPRESS means "only set it if you actually saw it".
#
# 3. set_defaults(handler=...). Without it you would need args.add_book
#    and args.return, and "return" is a Python keyword that cannot be
#    an attribute name. The handler mapping lets a command be called
#    whatever the language wants to call it.

def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--state", default=argparse.SUPPRESS,
                        help="where the shop is kept (default: shop.json)")
    common.add_argument("--quiet", action="store_true", default=argparse.SUPPRESS,
                        help="print nothing when it works")

    parser = argparse.ArgumentParser(
        prog="bookshop",
        description="Manage a bookshop: stock, members, loans and reports.",
        epilog="Exit codes: 0 worked, 1 refused, 2 the command was malformed.")
    parser.add_argument("--state", default="shop.json",
                        help="where the shop is kept (default: shop.json)")
    parser.add_argument("--quiet", action="store_true",
                        help="print nothing when it works")
    commands = parser.add_subparsers(dest="command", required=True)

    stock = commands.add_parser("add-book", parents=[common],
                                 help="put a new title in stock")
    stock.add_argument("title")
    stock.add_argument("author")
    stock.add_argument("--copies", type=int, default=1,
                       help="how many copies (default: 1)")
    stock.set_defaults(handler=cmd_add_book)

    people = commands.add_parser("add-member", parents=[common],
                                 help="register someone")
    people.add_argument("name")
    people.set_defaults(handler=cmd_add_member)

    borrow = commands.add_parser("borrow", parents=[common],
                                 help="lend a title to a member")
    borrow.add_argument("member")
    borrow.add_argument("title")
    borrow.add_argument("--day", type=int, required=True,
                        help="the day number the loan starts on")
    borrow.set_defaults(handler=cmd_borrow)

    give = commands.add_parser("return", parents=[common],
                               help="take a title back")
    give.add_argument("member")
    give.add_argument("title")
    give.add_argument("--day", type=int, required=True,
                      help="the day number it comes back on")
    give.set_defaults(handler=cmd_return)

    commands.add_parser("report", parents=[common],
                        help="print what the shop looks like").set_defaults(
        handler=cmd_report)

    out = commands.add_parser("export", parents=[common],
                              help="write the catalogue to a csv file")
    out.add_argument("path")
    out.set_defaults(handler=cmd_export)

    load = commands.add_parser("load", parents=[common],
                               help="replace the catalogue from a csv file")
    load.add_argument("path")
    load.set_defaults(handler=cmd_load)

    return parser


# ============================================================
# THE HANDLERS
# ============================================================
#
# Every handler returns an exit code. None of them calls sys.exit,
# because a function that kills the process cannot be called from a
# test to see what it would have done.

def announce(args, message):
    if not args.quiet:
        print(message)


def cmd_add_book(args):
    shop = load_state(args.state)
    shop.catalogue.add(args.title, args.author, args.copies)
    save_state(args.state, shop)
    announce(args, "stocked " + args.title.strip() + " x" + str(args.copies))
    return OK


def cmd_add_member(args):
    shop = load_state(args.state)
    shop.add_member(args.name)
    save_state(args.state, shop)
    announce(args, "welcome " + args.name.strip())
    return OK


def cmd_borrow(args):
    shop = load_state(args.state)
    shop.borrow(args.member, args.title, args.day)
    save_state(args.state, shop)
    announce(args, args.member + " has " + args.title + " until day " +
             str(args.day + shop.loan_days))
    return OK


def cmd_return(args):
    shop = load_state(args.state)
    fine = shop.give_back(args.member, args.title, args.day)
    save_state(args.state, shop)
    announce(args, "fine for " + args.title + " is " + str(fine))
    return OK


def cmd_report(args):
    shop = load_state(args.state)
    for line in shop.report():
        print(line)
    return OK


def cmd_export(args):
    shop = load_state(args.state)
    export_csv(args.path, shop.catalogue.rows())
    announce(args, "exported " + str(shop.catalogue.size()) + " title(s) to " + args.path)
    return OK


def cmd_load(args):
    shop = load_state(args.state)
    shop.catalogue.load_rows(import_csv(args.path))
    save_state(args.state, shop)
    announce(args, "loaded " + str(shop.catalogue.size()) + " title(s) from " + args.path)
    return OK


def main(argv):
    """argv is a list. That is the whole reason this is testable.

    argparse raises SystemExit(2) itself when the command makes no
    sense, and we let that through untouched, because 2 is argparse's
    code and we do not get to spend it twice. Our own refusals come
    back as the number 1."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except CliError as problem:
        print("error: " + str(problem), file=sys.stderr)
        return REFUSED


# ============================================================
# A HELPER THAT MAKES THE CLI CALLABLE FROM A TEST
# ============================================================

def run_cli(argv, columns=None):
    """Run one command with the streams captured, and report the exit
    code that a real terminal would have seen. No subprocess, no
    keyboard, no timing."""
    saved = os.environ.get("COLUMNS")
    if columns is not None:
        os.environ["COLUMNS"] = str(columns)
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = main(argv)
            except SystemExit as stop:
                code = stop.code
    finally:
        if saved is None:
            os.environ.pop("COLUMNS", None)
        else:
            os.environ["COLUMNS"] = saved
    return code, out.getvalue(), err.getvalue()


def lines_of(text):
    return [line for line in text.strip().splitlines() if line.strip()]


def scratch_state(folder, name="shop.json"):
    return os.path.join(folder, name)


def build_session(folder):
    """The four commands that make a shop worth reporting."""
    state = scratch_state(folder)
    run_cli(["add-book", "Dune", "Frank Herbert", "--copies", "3", "--state", state])
    run_cli(["add-book", "Clean Code, A Handbook", "Robert Martin",
             "--copies", "2", "--state", state])
    run_cli(["add-member", "Sara", "--state", state])
    run_cli(["add-member", "Ali", "--state", state])
    return state


# ============================================================
# PART A - THE QUESTIONS
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print("Q1  argv is a plain list, so main(argv) is a plain function")
print("Q2  that is what makes a terminal program testable at all")
print("Q3  the exit code is the part your shell actually reads")
print("Q4  so printing an error and exiting 0 is a lie with a straight face")
print("Q5  argparse spends 2 on its own mistakes, and 1 is yours to return")
print("Q6  data belongs on stdout and complaints belong on stderr")
print("Q7  a shared flag before the subcommand works, after it is rejected")
print("Q8  and the terminal width rewrites the help text, so never test it")
print()

print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  you can call main(['report', '--state', path]) and get a number")
print("Q1  no subprocess, no keyboard, no waiting, no flake")
print("Q2  a test that needs a human is a test that gets skipped")
print("Q3  bash, make and every CI system branch on it, not on your prose")
print("Q4  a script that pipes your output cannot tell the difference")
print("Q5  so argparse exits 2, and your handlers return 1, never both 2")
print("Q6  bookshop report > report.txt must contain data and no complaints")
print("Q7  because --state after 'report' is an argument report never had")
print("Q8  so a help test should assert the exit code, not the wording")
print("Q8  the wording changes with COLUMNS and between Python versions")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - the parser and its help")
print("T1  the commands it offers -> 7")
print("T1  asking for help exits -> 0")
print("T1  and the help landed on stdout -> True")
print("T1  the same help at 40 and 200 columns is identical -> False")
print("T1  help lines at 200 columns -> 20")
print("T1  help lines at 40 columns -> 34")
print("T1  so the wording is untestable, the exit code is not -> True")
print()

print("TASK 2 - who owns which exit code")
print("T2  a command that works exits -> 0")
print("T2  an unknown command exits -> 2")
print("T2  a missing required flag exits -> 2")
print("T2  a count that is not a number exits -> 2")
print("T2  no command at all exits -> 2")
print("T2  a command we understood and refused exits -> 1")
print("T2  so argparse owns 2 and you own 1 -> True")
print()

print("TASK 3 - stdout is for data, stderr is for complaints")
print("T3  the report wrote this many lines to stdout -> 3")
print("T3  and nothing at all to stderr -> True")
print("T3  a refusal wrote this many lines to stdout -> 0")
print("T3  and this to stderr -> error: not a member: Ghost")
print("T3  so bookshop report > f.txt captures data only -> True")
print()

print("TASK 4 - add-book, and who validates what")
print("T4  the default number of copies -> 1")
print("T4  an explicit count is stored -> 5")
print("T4  the title as stored -> 'Dune'")
print("T4  a count of three words exits -> 2")
print("T4  and argparse named the option -> True")
print("T4  a title of three spaces exits -> 1")
print("T4  because argparse cannot know what a real title is -> True")
print()

print("TASK 5 - borrow and return")
print("T5  borrowing as a member exits -> 0")
print("T5  the loan is due on day -> 24")
print("T5  borrowing as a stranger exits -> 1")
print("T5  and the message -> not a member: Ghost")
print("T5  returning it late costs -> 12")
print("T5  returning it twice exits -> 1")
print("T5  and the fine survived the save -> 12")
print()

print("TASK 6 - report and export")
print("T6  the report has this many lines -> 3")
print("T6  its first line -> books 2  members 2  open loans 0")
print("T6  the exported file has this many lines -> 3")
print("T6  and its header is -> title,author,copies")
print("T6  a title holding a comma round trips -> Clean Code, A Handbook")
print("T6  --quiet prints this -> ''")
print()

print("TASK 7 - the state file")
print("T7  the state file exists -> True")
print("T7  its keys come out sorted -> True")
print("T7  reloading gives the same titles -> ['Clean Code, A Handbook', 'Dune']")
print("T7  and the same fines -> 12")
print("T7  saving twice gives byte identical text -> True")
print("T7  a missing state file is not an error -> 0")
print()

print("TASK 8 - the trap, and the fix")
print("T8  the naive parser, --state before the command -> given.json")
print("T8  the naive parser, --state after the command -> exit 2 (rejected)")
print("T8  so the obvious fix is to share it with every subcommand")
print("T8  that fix, --state before the command -> shop.json  <- asked for given.json")
print("T8  and it exited cleanly while ignoring it -> True")
print("T8  that fix, --state after the command -> given.json")
print("T8  the real parser, --state before the command -> given.json")
print("T8  the real parser, --state after the command -> given.json")
print("T8  so SUPPRESS is the whole difference -> True")
print()

print("TASK 9 - the test suite")
print("T9   exit codes    passed   7  failed   0")
print("T9   streams       passed   5  failed   0")
print("T9   commands      passed   7  failed   0")
print("T9   persistence   passed   6  failed   0")
print("T9   TOTAL      passed  25  failed   0")
print("T9   errors -> 0")
print()

print("TASK 10 - the whole session")
print("T10   commands run -> 9")
print("T10   and the ones that refused -> 2")
print("T10   the final report -> books 3  members 2  open loans 0")
print("T10   total fines collected -> 12")
print("T10   the only exit code that was not zero -> [1]")
print("T10   and wrote nothing outside its folder -> True")
print()

print("=" * 60)


# ============================================================
# PART C - THE SOLUTION
# ============================================================

print()
print("=" * 60)
print("PART C - the solution")
print("=" * 60)

# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print()
print("-" * 60)
print("TASK 1 - the parser and its help")
print("-" * 60)
folder = tempfile.mkdtemp(prefix="project39_")
help_code, help_wide, _ = run_cli(["--help"], columns=200)
_, help_narrow, _ = run_cli(["--help"], columns=40)
command_words = ["add-book", "add-member", "borrow", "return",
                 "report", "export", "load"]
print("T1  the commands it offers ->",
      len([word for word in command_words if word in help_wide]))
print("T1  asking for help exits ->", help_code)
print("T1  and the help landed on stdout ->", "add-book" in help_wide)
print("T1  the same help at 40 and 200 columns is identical ->",
      help_wide == help_narrow)
print("T1  help lines at 200 columns ->", len(help_wide.splitlines()))
print("T1  help lines at 40 columns ->", len(help_narrow.splitlines()))
print("T1  so the wording is untestable, the exit code is not ->", help_code == 0)
print()

# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - who owns which exit code")
print("-" * 60)
state = build_session(folder)
checks = [
    ("a command that works", ["report", "--state", state]),
    ("an unknown command", ["fly", "--state", state]),
    ("a missing required flag", ["borrow", "Sara", "Dune", "--state", state]),
    ("a count that is not a number", ["add-book", "X", "Y", "--copies", "lots",
                                      "--state", state]),
    ("no command at all", []),
    ("a command we understood and refused", ["borrow", "Ghost", "Dune",
                                             "--day", "10", "--state", state]),
]
results = {}
for label, argv in checks:
    code, _, _ = run_cli(argv)
    results[label] = code
print("T2  a command that works exits ->", results["a command that works"])
print("T2  an unknown command exits ->", results["an unknown command"])
print("T2  a missing required flag exits ->", results["a missing required flag"])
print("T2  a count that is not a number exits ->",
      results["a count that is not a number"])
print("T2  no command at all exits ->", results["no command at all"])
print("T2  a command we understood and refused exits ->",
      results["a command we understood and refused"])
print("T2  so argparse owns 2 and you own 1 ->",
      results["an unknown command"] == USAGE and
      results["a command we understood and refused"] == REFUSED)
print()

# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - stdout is for data, stderr is for complaints")
print("-" * 60)
report_code, report_out, report_err = run_cli(["report", "--state", state])
print("T3  the report wrote this many lines to stdout ->",
      len(lines_of(report_out)))
print("T3  and nothing at all to stderr ->", report_err == "")
refuse_code, refuse_out, refuse_err = run_cli(
    ["borrow", "Ghost", "Dune", "--day", "10", "--state", state])
print("T3  a refusal wrote this many lines to stdout ->",
      len(lines_of(refuse_out)))
print("T3  and this to stderr ->", lines_of(refuse_err)[0])
print("T3  so bookshop report > f.txt captures data only ->",
      report_code == OK and report_err == "")
print()

# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - add-book, and who validates what")
print("-" * 60)
plain = scratch_state(folder, "plain.json")
run_cli(["add-book", "Solo", "Someone", "--state", plain])
solo_shop = load_state(plain)
print("T4  the default number of copies ->", solo_shop.catalogue.books["Solo"]["copies"])
run_cli(["add-book", "Dune", "Frank Herbert", "--copies", "5", "--state", plain])
print("T4  an explicit count is stored ->",
      load_state(plain).catalogue.books["Dune"]["copies"])
print("T4  the title as stored ->",
      repr(load_state(plain).catalogue.books["Dune"]["title"]))
bad_number, _, bad_err = run_cli(["add-book", "New", "One", "--copies", "lots",
                                  "--state", plain])
print("T4  a count of three words exits ->", bad_number)
print("T4  and argparse named the option ->", "--copies" in bad_err)
blank_code, _, blank_err = run_cli(["add-book", "   ", "Someone", "--state", plain])
print("T4  a title of three spaces exits ->", blank_code)
print("T4  because argparse cannot know what a real title is ->",
      blank_code == REFUSED and "title" in blank_err)
print()

# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - borrow and return")
print("-" * 60)
borrow_code, _, _ = run_cli(["borrow", "Sara", "Dune", "--day", "10", "--state", state])
print("T5  borrowing as a member exits ->", borrow_code)
print("T5  the loan is due on day ->", load_state(state).loans[("Sara", "Dune")])
stranger_code, _, stranger_err = run_cli(
    ["borrow", "Ghost", "Dune", "--day", "10", "--state", state])
print("T5  borrowing as a stranger exits ->", stranger_code)
print("T5  and the message ->", lines_of(stranger_err)[0].replace("error: ", ""))
late_code, late_out, _ = run_cli(
    ["return", "Sara", "Dune", "--day", "30", "--state", state])
print("T5  returning it late costs ->", lines_of(late_out)[0].split()[-1])
twice_code, _, twice_err = run_cli(
    ["return", "Sara", "Dune", "--day", "31", "--state", state])
print("T5  returning it twice exits ->", twice_code)
print("T5  and the fine survived the save ->",
      load_state(state).fines[0]["fine"])
print()

# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - report and export")
print("-" * 60)
_, six_out, _ = run_cli(["report", "--state", state])
six_lines = lines_of(six_out)
print("T6  the report has this many lines ->", len(six_lines))
print("T6  its first line ->", six_lines[0])
csv_path = os.path.join(folder, "catalogue.csv")
run_cli(["export", csv_path, "--state", state])
with open(csv_path, encoding="utf-8", newline="") as stream:
    csv_lines = stream.read().splitlines()
print("T6  the exported file has this many lines ->", len(csv_lines))
print("T6  and its header is ->", csv_lines[0])
round_tripped = Catalogue()
round_tripped.load_rows(import_csv(csv_path))
print("T6  a title holding a comma round trips ->",
      round_tripped.books["Clean Code, A Handbook"]["title"])
_, quiet_out, _ = run_cli(["export", os.path.join(folder, "again.csv"),
                           "--state", state, "--quiet"])
print("T6  --quiet prints this ->", repr(quiet_out))
print()

# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - the state file")
print("-" * 60)
with open(state, encoding="utf-8") as stream:
    state_text = stream.read()
print("T7  the state file exists ->", os.path.exists(state))
print("T7  its keys come out sorted ->",
      state_text.index('"books"') < state_text.index('"fines"') <
      state_text.index('"loans"') < state_text.index('"members"'))
reloaded = load_state(state)
print("T7  reloading gives the same titles ->", reloaded.catalogue.titles())
print("T7  and the same fines ->", reloaded.fines[0]["fine"])
first_text = dumps_canonical(reloaded.to_dict())
save_state(state, reloaded)
with open(state, encoding="utf-8") as stream:
    second_text = stream.read()
print("T7  saving twice gives byte identical text ->",
      first_text == second_text)
print("T7  a missing state file is not an error ->",
      load_state(os.path.join(folder, "never-written.json")).catalogue.size())
print()

# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - the trap, and the fix")
print("-" * 60)


def naive_parser(mode):
    """Three ways to hang one shared flag on a parser, so the lesson can
    be watched instead of believed."""
    parser = argparse.ArgumentParser(prog="bookshop")
    parser.add_argument("--state", default="shop.json")
    shared = argparse.ArgumentParser(add_help=False)
    if mode == "shared-plain":
        shared.add_argument("--state", default="shop.json")
    elif mode == "shared-suppressed":
        shared.add_argument("--state", default=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("report", parents=[] if mode == "top" else [shared])
    return parser


def parse_with(parser, argv):
    """argparse writes its complaint to stderr before it gives up, and
    that complaint is supposed to reach the terminal. Here it must not,
    so it is caught and thrown away."""
    with contextlib.redirect_stderr(io.StringIO()):
        try:
            return parser.parse_args(argv).state, None
        except SystemExit:
            return None, USAGE


top_before, _ = parse_with(naive_parser("top"), ["--state", "given.json", "report"])
top_after, top_code = parse_with(naive_parser("top"), ["report", "--state", "given.json"])
print("T8  the naive parser, --state before the command ->", top_before)
print("T8  the naive parser, --state after the command -> exit", top_code, "(rejected)")
print("T8  so the obvious fix is to share it with every subcommand")
plain_before, _ = parse_with(naive_parser("shared-plain"),
                             ["--state", "given.json", "report"])
plain_after, _ = parse_with(naive_parser("shared-plain"),
                            ["report", "--state", "given.json"])
print("T8  that fix, --state before the command ->", plain_before, " <- asked for given.json")
print("T8  and it exited cleanly while ignoring it ->", plain_before == "shop.json")
print("T8  that fix, --state after the command ->", plain_after)
real_before, _ = parse_with(build_parser(), ["--state", "given.json", "report"])
real_after, _ = parse_with(build_parser(), ["report", "--state", "given.json"])
print("T8  the real parser, --state before the command ->", real_before)
print("T8  the real parser, --state after the command ->", real_after)
print("T8  so SUPPRESS is the whole difference ->", real_before == real_after == "given.json")
print()

# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - the test suite")
print("-" * 60)


class ExitCodeTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp(prefix="project39_test_")
        self.state = build_session(self.folder)

    def tearDown(self):
        for name in os.listdir(self.folder):
            os.unlink(os.path.join(self.folder, name))
        os.rmdir(self.folder)

    def test_a_good_command_is_zero(self):
        self.assertEqual(run_cli(["report", "--state", self.state])[0], OK)

    def test_an_unknown_command_is_two(self):
        self.assertEqual(run_cli(["fly", "--state", self.state])[0], USAGE)

    def test_a_missing_flag_is_two(self):
        code, _, _ = run_cli(["borrow", "Sara", "Dune", "--state", self.state])
        self.assertEqual(code, USAGE)

    def test_a_wrong_type_is_two(self):
        code, _, _ = run_cli(["add-book", "A", "B", "--copies", "lots",
                              "--state", self.state])
        self.assertEqual(code, USAGE)

    def test_no_command_is_two(self):
        self.assertEqual(run_cli([])[0], USAGE)

    def test_a_refusal_is_one(self):
        code, _, _ = run_cli(["borrow", "Ghost", "Dune", "--day", "1",
                              "--state", self.state])
        self.assertEqual(code, REFUSED)

    def test_asking_for_help_is_zero(self):
        self.assertEqual(run_cli(["--help"])[0], OK)


class StreamTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp(prefix="project39_streams_")
        self.state = build_session(self.folder)

    def tearDown(self):
        for name in os.listdir(self.folder):
            os.unlink(os.path.join(self.folder, name))
        os.rmdir(self.folder)

    def test_report_writes_nothing_to_stderr(self):
        code, out, err = run_cli(["report", "--state", self.state])
        self.assertEqual((code, err), (OK, ""))

    def test_a_refusal_writes_nothing_to_stdout(self):
        code, out, err = run_cli(["borrow", "Ghost", "Dune", "--day", "1",
                                  "--state", self.state])
        self.assertEqual(out, "")

    def test_a_refusal_explains_itself(self):
        _, _, err = run_cli(["borrow", "Ghost", "Dune", "--day", "1",
                             "--state", self.state])
        self.assertIn("not a member", err)

    def test_quiet_stops_the_confirmation(self):
        path = os.path.join(self.folder, "quiet.csv")
        code, out, err = run_cli(["export", path, "--state", self.state, "--quiet"])
        self.assertEqual((code, out, err), (OK, "", ""))

    def test_without_quiet_it_speaks(self):
        path = os.path.join(self.folder, "loud.csv")
        _, out, _ = run_cli(["export", path, "--state", self.state])
        self.assertIn("exported", out)


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp(prefix="project39_cmds_")
        self.state = scratch_state(self.folder)

    def tearDown(self):
        for name in os.listdir(self.folder):
            os.unlink(os.path.join(self.folder, name))
        os.rmdir(self.folder)

    def test_a_book_takes_the_default_copies(self):
        run_cli(["add-book", "Solo", "Someone", "--state", self.state])
        self.assertEqual(load_state(self.state).catalogue.books["Solo"]["copies"], 1)

    def test_a_blank_title_is_refused_by_us(self):
        code, _, err = run_cli(["add-book", "   ", "Someone", "--state", self.state])
        self.assertEqual((code, "title" in err), (REFUSED, True))

    def test_a_duplicate_title_is_refused(self):
        run_cli(["add-book", "Solo", "Someone", "--state", self.state])
        code, _, _ = run_cli(["add-book", "Solo", "Other", "--state", self.state])
        self.assertEqual(code, REFUSED)

    def test_borrowing_then_returning_records_the_fine(self):
        run_cli(["add-book", "Dune", "Herbert", "--state", self.state])
        run_cli(["add-member", "Sara", "--state", self.state])
        run_cli(["borrow", "Sara", "Dune", "--day", "10", "--state", self.state])
        run_cli(["return", "Sara", "Dune", "--day", "30", "--state", self.state])
        self.assertEqual(load_state(self.state).fines[0]["fine"], 12)

    def test_state_works_in_either_position(self):
        """The whole point of SUPPRESS: whichever side of the command
        the user types it on, the same file is chosen."""
        self.assertEqual(run_cli(["--state", self.state, "report"])[0], OK)
        self.assertEqual(run_cli(["report", "--state", self.state])[0], OK)

    def test_the_naive_shared_flag_would_have_lost_the_value(self):
        shared = argparse.ArgumentParser(add_help=False)
        shared.add_argument("--state", default="shop.json")
        parser = argparse.ArgumentParser(prog="bookshop")
        parser.add_argument("--state", default="shop.json")
        sub = parser.add_subparsers(dest="command", required=True)
        sub.add_parser("report", parents=[shared])
        parsed = parser.parse_args(["--state", "given.json", "report"])
        self.assertEqual(parsed.state, "shop.json")
        self.assertEqual(build_parser().parse_args(
            ["--state", "given.json", "report"]).state, "given.json")

    def test_export_then_load_restores_the_catalogue(self):
        run_cli(["add-book", "Clean Code, A Handbook", "Martin",
                 "--state", self.state])
        path = os.path.join(self.folder, "c.csv")
        run_cli(["export", path, "--state", self.state])
        run_cli(["load", path, "--state", self.state])
        self.assertEqual(load_state(self.state).catalogue.titles(),
                         ["Clean Code, A Handbook"])


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp(prefix="project39_save_")
        self.state = build_session(self.folder)

    def tearDown(self):
        for name in os.listdir(self.folder):
            os.unlink(os.path.join(self.folder, name))
        os.rmdir(self.folder)

    def test_a_missing_state_file_starts_an_empty_shop(self):
        self.assertEqual(load_state(os.path.join(self.folder, "no.json"))
                         .catalogue.size(), 0)

    def test_the_keys_are_sorted_on_disk(self):
        with open(self.state, encoding="utf-8") as stream:
            text = stream.read()
        self.assertEqual(text, dumps_canonical(load_state(self.state).to_dict()))

    def test_saving_twice_gives_the_same_bytes(self):
        shop = load_state(self.state)
        before = dumps_canonical(shop.to_dict())
        save_state(self.state, shop)
        with open(self.state, encoding="utf-8") as stream:
            self.assertEqual(stream.read(), before)

    def test_no_temporary_file_survives(self):
        save_state(self.state, load_state(self.state))
        self.assertEqual([n for n in os.listdir(self.folder) if n.endswith(".tmp")], [])

    def test_the_fines_survive_a_reload(self):
        run_cli(["borrow", "Sara", "Dune", "--day", "10", "--state", self.state])
        run_cli(["return", "Sara", "Dune", "--day", "30", "--state", self.state])
        self.assertEqual(load_state(self.state).fines[0]["fine"], 12)

    def test_the_state_file_is_not_a_list(self):
        path = os.path.join(self.folder, "bad.json")
        with open(path, "w", encoding="utf-8") as stream:
            stream.write("[1, 2, 3]")
        self.assertEqual(run_cli(["report", "--state", path])[0], REFUSED)


SUITES = [("exit codes", ExitCodeTests),
          ("streams", StreamTests),
          ("commands", CommandTests),
          ("persistence", PersistenceTests)]

total_passed = 0
total_failed = 0
total_errors = 0
for label, suite in SUITES:
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(
        unittest.TestLoader().loadTestsFromTestCase(suite))
    good = result.testsRun - len(result.failures) - len(result.errors)
    print("T9  ", label.ljust(13), "passed", str(good).rjust(3),
          " failed", str(len(result.failures)).rjust(3))
    total_passed += good
    total_failed += len(result.failures)
    total_errors += len(result.errors)
print("T9   TOTAL".ljust(15), "passed", str(total_passed).rjust(3),
      " failed", str(total_failed).rjust(3))
print("T9   errors ->", total_errors)
print()

# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the whole session")
print("-" * 60)
session_folder = tempfile.mkdtemp(prefix="project39_session_")
session_state = scratch_state(session_folder)
SESSION = [
    ["add-book", "Dune", "Frank Herbert", "--copies", "3"],
    ["add-book", "Clean Code, A Handbook", "Robert Martin", "--copies", "2"],
    ["add-book", "Refactoring", "Martin Fowler", "--copies", "1"],
    ["add-member", "Sara"],
    ["add-member", "Ali"],
    ["borrow", "Sara", "Dune", "--day", "10"],
    ["borrow", "Ghost", "Dune", "--day", "10"],
    ["return", "Sara", "Dune", "--day", "30"],
    ["return", "Sara", "Dune", "--day", "31"],
]
refused = 0
exit_codes = []
for command in SESSION:
    code, _, _ = run_cli(command + ["--state", session_state, "--quiet"])
    exit_codes.append(code)
    if code != OK:
        refused += 1
_, session_out, _ = run_cli(["report", "--state", session_state])
finished = load_state(session_state)
print("T10   commands run ->", len(SESSION))
print("T10   and the ones that refused ->", refused)
print("T10   the final report ->", lines_of(session_out)[0])
print("T10   total fines collected ->",
      sum(fine["fine"] for fine in finished.fines))
print("T10   the only exit code that was not zero ->",
      sorted(set(code for code in exit_codes if code != OK)))
print("T10   and wrote nothing outside its folder ->",
      sorted(os.listdir(session_folder)) == ["shop.json"])
print()

for name in os.listdir(folder):
    os.unlink(os.path.join(folder, name))
os.rmdir(folder)
for name in os.listdir(session_folder):
    os.unlink(os.path.join(session_folder, name))
os.rmdir(session_folder)
print("=" * 60)
print("END OF PROJECT 39")
print("=" * 60)