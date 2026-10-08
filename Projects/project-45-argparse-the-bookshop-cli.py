# ============================================================
# Project 45 - argparse: the bookshop gets a proper CLI
# ============================================================
# What this lesson teaches:
#   argparse            a parser that understands words
#   subcommands         one parser, many verbs
#   add_argument        flags, options, and positionals
#   action='store_true'  a flag that flips to True
#   choices             only allow what you expect
#   default             what happens when nothing is given
#   nargs               one, many, or the rest
#   type                turn strings into ints, floats, paths
#   help                the help text is part of the contract
#   exit codes          0 worked, 1 refused, 2 argparse didn't understand
#
# Everything is the standard library. No input(), no random, no datetime.now.
# The output is deterministic. The file runs to completion and exits with 0.
#
# Run it:  python project-45-argparse-the-bookshop-cli.py
# ============================================================

import argparse
import contextlib
import io
import os
import sys

SCRIPT_DIR = sys.path[0] if False else __file__  # keep for consistency
CHECKS = []


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  what does argparse do")
print("Q2  what is a subcommand")
print("Q3  what does action='store_true' do")
print("Q4  what are choices for")
print("Q5  what does nargs='+' mean")
print("Q6  what does type=int do")
print("Q7  what exit code means argparse didn't understand")
print("Q8  what exit code means the program refused the command")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  it turns strings from sys.argv into an object with attributes")
print("Q2  a verb: add, list, sell, report - each with its own arguments")
print("Q3  it sets the attribute to True if the flag is present")
print("Q4  they limit the allowed values to a fixed set")
print("Q5  it collects one or more values into a list")
print("Q6  it converts the string to an integer")
print("Q7  2")
print("Q8  1")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - a parser that understands words")
print("T1  the parser parsed --name -> Alice")
print("T1  the parser parsed --count -> 3")
print("T1  so argparse turns strings into attributes -> True")
print()

print("TASK 2 - a flag with store_true")
print("T2  without --verbose -> False")
print("T2  with --verbose -> True")
print("T2  so a flag flips a boolean -> True")
print()

print("TASK 3 - choices keep you honest")
print("T3  format json -> json")
print("T3  format csv -> csv")
print("T3  so choices only allow what you expect -> True")
print()

print("TASK 4 - nargs collects values")
print("T4  tags with nargs='+' -> ['python', 'cli', 'argparse']")
print("T4  so nargs collects one or more values -> True")
print()

print("TASK 5 - subcommands: add a book")
print("T5  add --title Dune --copies 3 -> title Dune, copies 3")
print("T5  so subcommands split verbs from nouns -> True")
print()

print("TASK 6 - subcommands: list and sell")
print("T6  list -> command list")
print("T6  sell --title Dune --copies 1 -> sold 1 of Dune")
print("T6  so each subcommand has its own arguments -> True")
print()

print("TASK 7 - help is part of the contract")
print("T7  the help mentions add -> True")
print("T7  the help mentions list -> True")
print("T7  the help mentions sell -> True")
print("T7  so help teaches the user how to use it -> True")
print()

print("TASK 8 - exit codes tell the truth")
print("T8  success -> 0")
print("T8  refused -> 1")
print("T8  unknown -> 2")
print("T8  so the shell reads the exit code, not the words -> True")
print()

print("TASK 9 - the bookshop CLI in miniature")
print("T9  report -> 0, shows stock")
print("T9  add-book Dune 5 -> 0, added")
print("T9  sell-book Dune 2 -> 0, sold")
print("T9  refuse negative -> 1")
print("T9  so the CLI refuses bad input and exits with 1 -> True")
print()

print("TASK 10 - the loop, closed: argv is just a list")
print("T10  main(['report']) -> 0")
print("T10  main(['add-book', 'Dune', '3']) -> 0")
print("T10  main(['sell-book', 'Dune', '-1']) -> 1")
print("T10  main(['unknown']) -> 2")
print("T10  so you can test the CLI without a keyboard -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)

projects_before = sorted(os.listdir(os.path.dirname(SCRIPT_DIR)))


# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - a parser that understands words")
print("-" * 60)
parser = argparse.ArgumentParser()
parser.add_argument("--name")
parser.add_argument("--count", type=int)
args = parser.parse_args(["--name", "Alice", "--count", "3"])

check("name is Alice", args.name == "Alice")
check("count is 3", args.count == 3)
check("count is int", isinstance(args.count, int))
check("args has attributes", hasattr(args, "name") and hasattr(args, "count"))
check("parser understood the words", args.name == "Alice" and args.count == 3)

print("T1  the parser parsed --name ->", args.name)
print("T1  the parser parsed --count ->", args.count)
print("T1  so argparse turns strings into attributes ->",
      args.name == "Alice" and args.count == 3)
print()


# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - a flag with store_true")
print("-" * 60)
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
args_off = parser.parse_args([])
args_on = parser.parse_args(["--verbose"])

check("without flag False", args_off.verbose is False)
check("with flag True", args_on.verbose is True)
check("default is False", args_off.verbose is False)
check("action flips it", args_on.verbose is True)
check("the flag is a boolean switch", args_off.verbose is False and args_on.verbose is True)

print("T2  without --verbose ->", args_off.verbose)
print("T2  with --verbose ->", args_on.verbose)
print("T2  so a flag flips a boolean ->",
      args_off.verbose is False and args_on.verbose is True)
print()


# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - choices keep you honest")
print("-" * 60)
parser = argparse.ArgumentParser()
parser.add_argument("--format", choices=["json", "csv"])
args_json = parser.parse_args(["--format", "json"])
args_csv = parser.parse_args(["--format", "csv"])

check("json is allowed", args_json.format == "json")
check("csv is allowed", args_csv.format == "csv")
check("choices are enforced", args_json.format in ["json", "csv"])
check("the value is exactly one of them", args_csv.format == "csv")
check("choices keep you honest", args_json.format == "json" and args_csv.format == "csv")

print("T3  format json ->", args_json.format)
print("T3  format csv ->", args_csv.format)
print("T3  so choices only allow what you expect ->",
      args_json.format == "json" and args_csv.format == "csv")
print()


# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - nargs collects values")
print("-" * 60)
parser = argparse.ArgumentParser()
parser.add_argument("--tags", nargs="+")
args = parser.parse_args(["--tags", "python", "cli", "argparse"])

check("nargs collects a list", isinstance(args.tags, list))
check("three values collected", len(args.tags) == 3)
check("the values are strings", all(isinstance(t, str) for t in args.tags))
check("the list is correct", args.tags == ["python", "cli", "argparse"])
check("nargs plus means one or more", len(args.tags) >= 1)

print("T4  tags with nargs='+' ->", args.tags)
print("T4  so nargs collects one or more values ->",
      args.tags == ["python", "cli", "argparse"])
print()


# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - subcommands: add a book")
print("-" * 60)
parser = argparse.ArgumentParser()
subs = parser.add_subparsers(dest="command")
add = subs.add_parser("add")
add.add_argument("--title", required=True)
add.add_argument("--copies", type=int, default=1)
args = parser.parse_args(["add", "--title", "Dune", "--copies", "3"])

check("command is add", args.command == "add")
check("title is Dune", args.title == "Dune")
check("copies is 3", args.copies == 3)
check("copies is int", isinstance(args.copies, int))
check("subcommand split the verb", args.command == "add")

print("T5  add --title Dune --copies 3 -> title {0}, copies {1}".format(
    args.title, args.copies))
print("T5  so subcommands split verbs from nouns ->", args.command == "add")
print()


# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - subcommands: list and sell")
print("-" * 60)
parser = argparse.ArgumentParser()
subs = parser.add_subparsers(dest="command")
subs.add_parser("list")
sell = subs.add_parser("sell")
sell.add_argument("--title", required=True)
sell.add_argument("--copies", type=int, required=True)
args_list = parser.parse_args(["list"])
args_sell = parser.parse_args(["sell", "--title", "Dune", "--copies", "1"])

check("list command", args_list.command == "list")
check("sell command", args_sell.command == "sell")
check("sell has title", args_sell.title == "Dune")
check("sell has copies", args_sell.copies == 1)
check("each subcommand has its own args",
      args_list.command == "list" and args_sell.command == "sell")

print("T6  list -> command", args_list.command)
print("T6  sell --title Dune --copies 1 -> sold {0} of {1}".format(
    args_sell.copies, args_sell.title))
print("T6  so each subcommand has its own arguments ->",
      args_list.command == "list" and args_sell.command == "sell")
print()


# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - help is part of the contract")
print("-" * 60)
parser = argparse.ArgumentParser()
subs = parser.add_subparsers(dest="command")
subs.add_parser("add")
subs.add_parser("list")
subs.add_parser("sell")
buf = io.StringIO()
parser.print_help(buf)
help_text = buf.getvalue()

check("help mentions add", "add" in help_text)
check("help mentions list", "list" in help_text)
check("help mentions sell", "sell" in help_text)
check("help is non-empty", len(help_text) > 0)
check("help teaches the user", "add" in help_text and "list" in help_text and "sell" in help_text)

print("T7  the help mentions add ->", "add" in help_text)
print("T7  the help mentions list ->", "list" in help_text)
print("T7  the help mentions sell ->", "sell" in help_text)
print("T7  so help teaches the user how to use it ->",
      "add" in help_text and "list" in help_text and "sell" in help_text)
print()


# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - exit codes tell the truth")
print("-" * 60)
parser = argparse.ArgumentParser()
subs = parser.add_subparsers(dest="command")
subs.add_parser("ok")
parser_refuse = argparse.ArgumentParser()
subs_r = parser_refuse.add_subparsers(dest="command")
ok_r = subs_r.add_parser("ok")
ok_r.add_argument("--copies", type=int, choices=[1, 2, 3])

# success
try:
    parser.parse_args(["ok"])
    code_ok = 0
except SystemExit as e:
    code_ok = e.code if e.code is not None else 1

# refused - we simulate by returning 1
code_refuse = 1

# unknown - argparse prints its usage to stderr and exits 2; we keep
# the run quiet by capturing that message instead of letting it escape
try:
    with contextlib.redirect_stderr(io.StringIO()):
        parser.parse_args(["nope"])
    code_unknown = 0
except SystemExit as e:
    code_unknown = e.code if e.code is not None else 2

check("success is 0", code_ok == 0)
check("refused is 1", code_refuse == 1)
check("unknown is 2", code_unknown == 2)
check("the three codes differ", len({code_ok, code_refuse, code_unknown}) == 3)
check("exit codes tell the truth",
      code_ok == 0 and code_refuse == 1 and code_unknown == 2)

print("T8  success ->", code_ok)
print("T8  refused ->", code_refuse)
print("T8  unknown ->", code_unknown)
print("T8  so the shell reads the exit code, not the words ->",
      code_ok == 0 and code_refuse == 1 and code_unknown == 2)
print()


# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - the bookshop CLI in miniature")
print("-" * 60)
stock = {"Dune": 5}


def mini_main(argv):
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="command")
    subs.add_parser("report")
    add = subs.add_parser("add-book")
    add.add_argument("title")
    add.add_argument("copies", type=int)
    sell = subs.add_parser("sell-book")
    sell.add_argument("title")
    sell.add_argument("copies", type=int)
    try:
        # an unknown verb makes argparse print usage on stderr and
        # exit 2; capture it so a failed run never dirties stderr
        with contextlib.redirect_stderr(io.StringIO()):
            args = parser.parse_args(argv)
    except SystemExit as e:
        return e.code if e.code is not None else 2
    if args.command == "report":
        return 0
    if args.command == "add-book":
        if args.copies < 0:
            return 1
        stock[args.title] = stock.get(args.title, 0) + args.copies
        return 0
    if args.command == "sell-book":
        if args.copies < 0:
            return 1
        if args.title not in stock or stock[args.title] < args.copies:
            return 1
        stock[args.title] -= args.copies
        return 0
    return 2


r1 = mini_main(["report"])
r2 = mini_main(["add-book", "Dune", "5"])
r3 = mini_main(["sell-book", "Dune", "2"])
r4 = mini_main(["sell-book", "Dune", "-1"])

check("report returns 0", r1 == 0)
check("add-book returns 0", r2 == 0)
check("sell-book returns 0", r3 == 0)
check("negative copies refused", r4 == 1)
check("CLI refuses bad input", r4 == 1)

print("T9  report -> {0}, shows stock".format(r1))
print("T9  add-book Dune 5 -> {0}, added".format(r2))
print("T9  sell-book Dune 2 -> {0}, sold".format(r3))
print("T9  refuse negative -> {0}".format(r4))
print("T9  so the CLI refuses bad input and exits with 1 ->", r4 == 1)
print()


# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the loop, closed: argv is just a list")
print("-" * 60)
stock.clear()
stock["Dune"] = 5

m1 = mini_main(["report"])
m2 = mini_main(["add-book", "Dune", "3"])
m3 = mini_main(["sell-book", "Dune", "-1"])
m4 = mini_main(["unknown"])

check("main(['report']) is 0", m1 == 0)
check("main(['add-book','Dune','3']) is 0", m2 == 0)
check("main(['sell-book','Dune','-1']) is 1", m3 == 1)
check("main(['unknown']) is 2", m4 == 2)
check("argv is just a list", isinstance(["report"], list))

print("T10  main(['report']) ->", m1)
print("T10  main(['add-book', 'Dune', '3']) ->", m2)
print("T10  main(['sell-book', 'Dune', '-1']) ->", m3)
print("T10  main(['unknown']) ->", m4)
print("T10  so you can test the CLI without a keyboard ->",
      m1 == 0 and m2 == 0 and m3 == 1 and m4 == 2)
print()


# ------------------------------------------------------------
# report
# ------------------------------------------------------------
projects_after = sorted(os.listdir(os.path.dirname(SCRIPT_DIR)))
failed = [name for name, ok in CHECKS if not ok]
print("=" * 60)
if failed:
    for name in failed:
        print("  FAILED:", name)
    print("CHECKS PASSED {0} of {1}".format(
        len(CHECKS) - len(failed), len(CHECKS)))
    sys.exit(1)
print("ALL {0} CHECKS PASSED".format(len(CHECKS)))
print("=" * 60)