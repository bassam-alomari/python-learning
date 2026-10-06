# ============================================================
# Project 41 - packaging: pyproject.toml, a wheel, and an offline install
# ============================================================
# What this lesson teaches:
#   pyproject.toml    who you are, which tomllib parses for you
#   types             the quotes in TOML decide the Python type
#   a wheel           a .whl file is a zip with a fixed layout
#   METADATA / WHEEL  headers, read by email.parser like any RFC 822
#   RECORD            the sha256 and size of every file, recheckable
#   entry points      name = module:function becomes a command
#   pip --no-index    install from a folder, with the network removed
#   importlib.metadata  where the version really comes from
#
# Everything here is the standard library plus pip. No network is
# touched: pip is told --no-index, so it can only use the file we
# hand it. The wheel is built with zipfile, so you can open it with
# any zip tool and see every part of it.
#
# Run it:  python project-41-packaging-a-wheel.py
# ============================================================

import base64
import contextlib
import csv
import email.parser
import hashlib
import importlib
import importlib.metadata
import io
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import tomllib
import zipfile

FOLDER = tempfile.mkdtemp(prefix="project41_")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKS = []

NAME = "bookshop"
VERSION = "1.2.3"
DIST = "{0}-{1}.dist-info".format(NAME, VERSION)
WHEEL_NAME = "{0}-{1}-py3-none-any.whl".format(NAME, VERSION)

SRC = os.path.join(FOLDER, "src")
PACKAGE_DIR = os.path.join(SRC, NAME)
TARGET = os.path.join(FOLDER, "site")
WHEEL_PATH = os.path.join(FOLDER, WHEEL_NAME)
TAMPERED_PATH = os.path.join(FOLDER, "tampered-" + WHEEL_NAME)

PYPROJECT = '''[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "bookshop"
version = "1.2.3"
description = "A bookshop you can install"
requires-python = ">=3.11"
authors = [{name = "Python Learning", email = "nobody@example.com"}]

[project.scripts]
bookshop = "bookshop.cli:main"
'''

INIT_SOURCE = '''"""A bookshop you can install."""

__version__ = "1.2.3"
'''

CLI_SOURCE = '''"""The command line face of bookshop."""


def main():
    print("bookshop says hello")


def greet(name):
    return "hello " + name
'''

METADATA_SOURCE = '''Metadata-Version: 2.1
Name: bookshop
Version: 1.2.3
Summary: A bookshop you can install
Requires-Python: >=3.11
'''

WHEEL_SOURCE = '''Wheel-Version: 1.0
Generator: project-41 (1.0)
Root-Is-Purelib: true
Tag: py3-none-any
'''

ENTRY_SOURCE = '''[console_scripts]
bookshop = bookshop.cli:main
'''


def check(name, condition):
    """A claim this file is willing to be wrong about."""
    CHECKS.append((name, bool(condition)))
    return bool(condition)


def write(path, source):
    """Write one file with stable line endings, so hashes stay stable."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(source)
    return path


def purge():
    """Forget every copy of the package, so the next import starts clean."""
    for module in [m for m in list(sys.modules)
                   if m == NAME or m.startswith(NAME + ".")]:
        del sys.modules[module]


def digest_of(raw):
    """RECORD stores urlsafe base64 of sha256, with the padding removed."""
    return "sha256=" + base64.urlsafe_b64encode(
        hashlib.sha256(raw).digest()).rstrip(b"=").decode("ascii")


def build_wheel(path, package_files):
    """A wheel is a zip. Build one by hand and pip will accept it."""
    entries = dict(package_files)
    entries[DIST + "/METADATA"] = METADATA_SOURCE
    entries[DIST + "/WHEEL"] = WHEEL_SOURCE
    entries[DIST + "/entry_points.txt"] = ENTRY_SOURCE
    rows = []
    for name in sorted(entries):
        raw = entries[name].encode("utf-8")
        rows.append((name, digest_of(raw), len(raw)))
    record = "".join("{0},{1},{2}\n".format(*row) for row in rows)
    record += "{0}/RECORD,,\n".format(DIST)
    entries[DIST + "/RECORD"] = record
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(entries):
            archive.writestr(name, entries[name])
    return entries


def read_wheel(path):
    """Every byte inside the zip, keyed by its entry name."""
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def verify_record(path):
    """Recompute every hash RECORD claims. Returns (checked, broken)."""
    inside = read_wheel(path)
    checked = broken = 0
    for row in csv.reader(io.StringIO(
            inside[DIST + "/RECORD"].decode("utf-8"))):
        if not row[1]:
            continue
        checked += 1
        raw = inside[row[0]]
        if digest_of(raw) != row[1] or str(len(raw)) != row[2]:
            broken += 1
    return checked, broken


def console_script():
    """Where pip puts the command it writes for --target."""
    bin_dir = os.path.join(TARGET, "bin")
    if not os.path.isdir(bin_dir):
        return None
    for name in sorted(os.listdir(bin_dir)):
        if name.startswith(NAME) and not name.endswith(".py"):
            return os.path.join(bin_dir, name)
    return None


# ============================================================
# PART A - the questions
# ============================================================

print("=" * 60)
print("PART A - the questions")
print("=" * 60)
print()
print("Q1  which file tells a package builder who it is, and who reads it")
print("Q2  what Python type does tomllib give you for version = \"1.2.3\"")
print("Q3  what is a wheel, and what travels inside the file")
print("Q4  why must zip entry names use a forward slash even on Windows")
print("Q5  what does RECORD let you prove about a wheel you were handed")
print("Q6  where does the version of an installed package really come from")
print("Q7  what does one line in entry_points.txt turn into")
print("Q8  why does pip --target not put a command on your PATH")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  pyproject.toml, and tomllib has read it since Python 3.11")
print("Q2  a str, because the quotes are part of the format, not decoration")
print("Q3  a zip holding your package plus a name-version.dist-info folder")
print("Q4  the wheel spec says so, and a backslash unpacks wrong elsewhere")
print("Q5  the sha256 and size of every file, so you can recheck them")
print("Q6  importlib.metadata reads it out of the .dist-info folder")
print("Q7  name = module:function becomes a command pip writes for you")
print("Q8  --target is a folder, not an environment, so nothing joins PATH")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - pyproject.toml is a contract, and tomllib reads it")
print("T1  the parser hands back a -> dict")
print("T1  name -> bookshop")
print("T1  version -> 1.2.3")
print("T1  requires-python -> >=3.11")
print("T1  scripts -> {'bookshop': 'bookshop.cli:main'}")
print("T1  so the metadata is data, never a string you split -> True")
print()

print("TASK 2 - types are the whole point of a parser")
print("T2  unquoted 41 parses as -> int")
print("T2  quoted \"41\" parses as -> str")
print("T2  and version = \"1.2.3\" is quoted, so -> str")
print("T2  the scripts table is a -> dict")
print("T2  so quoting picks the type and TOML never guesses -> True")
print()

print("TASK 3 - the two files this package ships")
print("T3  bookshop/__init__.py holds this many lines -> 3")
print("T3  bookshop/cli.py holds this many lines -> 9")
print("T3  greet('sara') -> hello sara")
print("T3  so the code worked before anything was packaged -> True")
print()

print("TASK 4 - a wheel is a zip with a fixed layout")
print("T4  the wheel is named -> bookshop-1.2.3-py3-none-any.whl")
print("T4  it holds this many entries -> 6")
print("T4  the dist-info folder is -> bookshop-1.2.3.dist-info")
print("T4  every entry uses a forward slash -> True")
print("T4  a backslash in any entry name -> False")
print("T4  so you could open this wheel with any zip tool -> True")
print()

print("TASK 5 - METADATA and WHEEL are headers, not code")
print("T5  METADATA says Name -> bookshop")
print("T5  METADATA says Version -> 1.2.3")
print("T5  METADATA says Requires-Python -> >=3.11")
print("T5  WHEEL says Root-Is-Purelib -> true")
print("T5  WHEEL says Tag -> py3-none-any")
print("T5  so the description travels beside the code in plain text -> True")
print()

print("TASK 6 - RECORD is the manifest, and a manifest can be checked")
print("T6  RECORD hashes this many files -> 5")
print("T6  recomputing each sha256 matched -> 5")
print("T6  rebuild with one byte changed and the rows that break -> 1")
print("T6  so a wheel carries the proof that it is intact -> True")
print()

print("TASK 7 - an entry point is one line that becomes a command")
print("T7  entry_points.txt says -> bookshop = bookshop.cli:main")
print("T7  the command it names -> bookshop")
print("T7  it points at the module -> bookshop.cli")
print("T7  and the function -> main")
print("T7  loading and calling that function printed -> bookshop says hello")
print("T7  so the command in pyproject.toml is plain text, not magic -> True")
print()

print("TASK 8 - pip installs a local wheel with no network at all")
print("T8  the flag that removes the network -> --no-index")
print("T8  pip's exit code -> 0")
print("T8  pip printed nothing at all -> True")
print("T8  the command it wrote is on disk -> True")
print("T8  so a wheel installs straight from a folder -> True")
print()

print("TASK 9 - the installed copy answers to its name")
print("T9  it imported from -> bookshop/__init__.py")
print("T9  the code claims its version -> 1.2.3")
print("T9  importlib.metadata claims -> 1.2.3")
print("T9  pyproject.toml claims -> 1.2.3")
print("T9  all three version sources agree -> True")
print("T9  greet('sara') -> hello sara")
print()

print("TASK 10 - the loop, closed")
print("T10  the console script ran and exited -> 0")
print("T10  and printed -> bookshop says hello")
print("T10  the same script with no folder on the path -> 1")
print("T10  because --target is a folder, not an environment -> True")
print("T10  the wheel still imports straight from the zip -> True")
print("T10  and the folder this file lives in is untouched -> True")
print()


# ============================================================
# PART C - the solution
# ============================================================

print("=" * 60)
print("PART C - the solution")
print("=" * 60)

projects_before = sorted(os.listdir(SCRIPT_DIR))

# ------------------------------------------------------------
# TASK 1
# ------------------------------------------------------------
print("-" * 60)
print("TASK 1 - pyproject.toml is a contract, and tomllib reads it")
print("-" * 60)
document = tomllib.loads(PYPROJECT)
project = document["project"]
scripts = project["scripts"]

check("the TOML document parses to a dict", isinstance(document, dict))
check("the project table parses to a dict", isinstance(project, dict))
check("the name is bookshop", project["name"] == NAME)
check("the version is 1.2.3", project["version"] == VERSION)
check("requires-python is >=3.11", project["requires-python"] == ">=3.11")
check("the scripts table has one entry", len(scripts) == 1)

print("T1  the parser hands back a ->", type(document).__name__)
print("T1  name ->", project["name"])
print("T1  version ->", project["version"])
print("T1  requires-python ->", project["requires-python"])
print("T1  scripts ->", repr(scripts))
print("T1  so the metadata is data, never a string you split ->",
      isinstance(scripts, dict))
print()

# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - types are the whole point of a parser")
print("-" * 60)
unquoted = tomllib.loads("value = 41")["value"]
quoted = tomllib.loads('value = "41"')["value"]

check("unquoted 41 becomes an int", type(unquoted) is int)
check('quoted "41" becomes a str', type(quoted) is str)
check("the version stays a str", type(project["version"]) is str)
check("the scripts table stays a dict", type(scripts) is dict)
check("the authors is a list of tables", isinstance(project["authors"], list))

print("T2  unquoted 41 parses as ->", type(unquoted).__name__)
print("T2  quoted \"41\" parses as ->", type(quoted).__name__)
print("T2  and version = \"1.2.3\" is quoted, so ->",
      type(project["version"]).__name__)
print("T2  the scripts table is a ->", type(scripts).__name__)
print("T2  so quoting picks the type and TOML never guesses ->",
      type(unquoted) is int and type(quoted) is str)
print()

# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - the two files this package ships")
print("-" * 60)
init_path = write(os.path.join(PACKAGE_DIR, "__init__.py"), INIT_SOURCE)
cli_path = write(os.path.join(PACKAGE_DIR, "cli.py"), CLI_SOURCE)

sys.path.insert(0, SRC)
import bookshop as from_source                      # noqa: E402
source_cli = importlib.import_module(NAME + ".cli")
source_greet = source_cli.greet("sara")
source_version = from_source.__version__
purge()
sys.path.remove(SRC)

init_lines = len(INIT_SOURCE.splitlines())
cli_lines = len(CLI_SOURCE.splitlines())

check("__init__.py holds three lines", init_lines == 3)
check("cli.py holds nine lines", cli_lines == 9)
check("the source package imported", source_version == VERSION)
check("greet works before packaging", source_greet == "hello sara")
check("both files were written", os.path.exists(init_path) and
      os.path.exists(cli_path))

print("T3  bookshop/__init__.py holds this many lines ->", init_lines)
print("T3  bookshop/cli.py holds this many lines ->", cli_lines)
print("T3  greet('sara') ->", source_greet)
print("T3  so the code worked before anything was packaged ->",
      source_greet == "hello sara" and source_version == VERSION)
print()

# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - a wheel is a zip with a fixed layout")
print("-" * 60)
package_files = {
    "{0}/__init__.py".format(NAME): INIT_SOURCE,
    "{0}/cli.py".format(NAME): CLI_SOURCE,
}
entries = build_wheel(WHEEL_PATH, package_files)
names = sorted(entries)

check("the wheel file exists", os.path.exists(WHEEL_PATH))
check("the wheel holds six entries", len(names) == 6)
check("every entry has a forward slash", all("/" in n for n in names))
check("no entry name holds a backslash", not any("\\" in n for n in names))
check("the zip is intact", zipfile.ZipFile(WHEEL_PATH).testzip() is None)

print("T4  the wheel is named ->", WHEEL_NAME)
print("T4  it holds this many entries ->", len(names))
print("T4  the dist-info folder is ->", DIST)
print("T4  every entry uses a forward slash ->", all("/" in n for n in names))
print("T4  a backslash in any entry name ->", any("\\" in n for n in names))
print("T4  so you could open this wheel with any zip tool ->",
      zipfile.ZipFile(WHEEL_PATH).testzip() is None)
print()

# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - METADATA and WHEEL are headers, not code")
print("-" * 60)
inside = read_wheel(WHEEL_PATH)
metadata_text = inside[DIST + "/METADATA"].decode("utf-8")
wheel_text = inside[DIST + "/WHEEL"].decode("utf-8")
metadata = email.parser.Parser().parsestr(metadata_text)
wheel_headers = email.parser.Parser().parsestr(wheel_text)

check("METADATA names bookshop", metadata["Name"] == NAME)
check("METADATA versions 1.2.3", metadata["Version"] == VERSION)
check("METADATA requires >=3.11", metadata["Requires-Python"] == ">=3.11")
check("WHEEL is purelib", wheel_headers["Root-Is-Purelib"] == "true")
check("WHEEL tags py3-none-any", wheel_headers["Tag"] == "py3-none-any")
check("Metadata-Version is 2.1", metadata["Metadata-Version"] == "2.1")

print("T5  METADATA says Name ->", metadata["Name"])
print("T5  METADATA says Version ->", metadata["Version"])
print("T5  METADATA says Requires-Python ->", metadata["Requires-Python"])
print("T5  WHEEL says Root-Is-Purelib ->", wheel_headers["Root-Is-Purelib"])
print("T5  WHEEL says Tag ->", wheel_headers["Tag"])
print("T5  so the description travels beside the code in plain text ->",
      metadata["Name"] == NAME and metadata["Version"] == VERSION)
print()

# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - RECORD is the manifest, and a manifest can be checked")
print("-" * 60)
record_text = inside[DIST + "/RECORD"].decode("utf-8")
record_rows = [row for row in csv.reader(io.StringIO(record_text)) if row[1]]
checked, broken = verify_record(WHEEL_PATH)

# the attack worth detecting: a file edited inside the wheel, with the
# original RECORD left in place. build_wheel() would have re-signed it,
# so this copies the wheel byte for byte and changes only cli.py.
tampered_files = dict(entries)
with zipfile.ZipFile(TAMPERED_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
    for name in sorted(tampered_files):
        payload = tampered_files[name]
        if name == "{0}/cli.py".format(NAME):
            payload = payload + " "
        archive.writestr(name, payload)
tampered_checked, tampered_broken = verify_record(TAMPERED_PATH)

check("RECORD hashes five files", checked == 5)
check("the real wheel is unbroken", broken == 0)
check("the tampered wheel checks the same five rows", tampered_checked == 5)
check("one changed byte breaks exactly one row", tampered_broken == 1)
check("RECORD hashes the two package files",
      any(row[0] == "{0}/cli.py".format(NAME) for row in record_rows))

print("T6  RECORD hashes this many files ->", checked)
print("T6  recomputing each sha256 matched ->", checked - broken)
print("T6  rebuild with one byte changed and the rows that break ->",
      tampered_broken)
print("T6  so a wheel carries the proof that it is intact ->",
      broken == 0 and tampered_broken == 1)
print()

# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - an entry point is one line that becomes a command")
print("-" * 60)
section = None
point = None
for line in inside[DIST + "/entry_points.txt"].decode("utf-8").splitlines():
    stripped = line.strip()
    if stripped.startswith("["):
        section = stripped.strip("[]")
    elif "=" in stripped and section == "console_scripts":
        point = [part.strip() for part in stripped.split("=", 1)]
command, target = point
module_name, function_name = target.split(":", 1)

# the entry point names a module - import it from the wheel itself
purge()
sys.path.insert(0, WHEEL_PATH)
module = importlib.import_module(module_name)
loaded = getattr(module, function_name)
buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    loaded()
printed = buffer.getvalue().strip()
purge()
sys.path.remove(WHEEL_PATH)

check("one console script is declared", command == NAME)
check("it points at bookshop.cli", module_name == "bookshop.cli")
check("it points at main", function_name == "main")
check("the module imports from the wheel", "whl" in module.__file__)
check("calling it prints the greeting", printed == "bookshop says hello")

print("T7  entry_points.txt says ->", command, "=", target)
print("T7  the command it names ->", command)
print("T7  it points at the module ->", module_name)
print("T7  and the function ->", function_name)
print("T7  loading and calling that function printed ->", printed)
print("T7  so the command in pyproject.toml is plain text, not magic ->",
      printed == "bookshop says hello")
print()

# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - pip installs a local wheel with no network at all")
print("-" * 60)
command_line = [sys.executable, "-m", "pip", "install", "--no-index",
                "--disable-pip-version-check", "--quiet",
                "--target", TARGET, WHEEL_PATH]
installed = subprocess.run(command_line, capture_output=True, text=True,
                           encoding="utf-8")
script = console_script()
silent = not installed.stdout.strip() and not installed.stderr.strip()

check("pip exited zero", installed.returncode == 0)
check("pip printed nothing", silent)
check("the wheel went into the target folder",
      os.path.isdir(os.path.join(TARGET, NAME)))
check("pip wrote a dist-info folder",
      os.path.isdir(os.path.join(TARGET, DIST)))
check("pip wrote the command", script is not None)
check("pip never needed the network", "--no-index" in command_line)

print("T8  the flag that removes the network -> --no-index")
print("T8  pip's exit code ->", installed.returncode)
print("T8  pip printed nothing at all ->", silent)
print("T8  the command it wrote is on disk ->", script is not None)
print("T8  so a wheel installs straight from a folder ->",
      installed.returncode == 0 and silent)
print()

# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - the installed copy answers to its name")
print("-" * 60)
sys.path.insert(0, TARGET)
import bookshop as from_target                    # noqa: E402
installed_cli = importlib.import_module(NAME + ".cli")
installed_greet = installed_cli.greet("sara")
code_version = from_target.__version__
metadata_version = importlib.metadata.version(NAME)
toml_version = project["version"]
imported_from = os.path.relpath(from_target.__file__, TARGET)
imported_from = imported_from.replace(os.sep, "/")
purge()

agree = code_version == metadata_version == toml_version == VERSION

check("the installed package imports", code_version == VERSION)
check("importlib.metadata agrees", metadata_version == VERSION)
check("pyproject.toml agrees", toml_version == VERSION)
check("all three agree", agree)
check("it imported from the target folder", imported_from.startswith(NAME + "/"))
check("greet still works installed", installed_greet == "hello sara")

print("T9  it imported from ->", imported_from)
print("T9  the code claims its version ->", code_version)
print("T9  importlib.metadata claims ->", metadata_version)
print("T9  pyproject.toml claims ->", toml_version)
print("T9  all three version sources agree ->", agree)
print("T9  greet('sara') ->", installed_greet)
print()

# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the loop, closed")
print("-" * 60)
with_path = dict(os.environ, PYTHONPATH=TARGET)
without_path = {key: value for key, value in os.environ.items()
                if key.upper() != "PYTHONPATH"}
ran = subprocess.run([script], capture_output=True, text=True,
                     encoding="utf-8", env=with_path)
ran_alone = subprocess.run([script], capture_output=True, text=True,
                           encoding="utf-8", env=without_path)

# the wheel still stands on its own, with nothing installed
purge()
sys.path.remove(TARGET)
sys.path.insert(0, WHEEL_PATH)
import bookshop as from_zip                      # noqa: E402
zip_imported = ".whl" in from_zip.__file__
zip_version = from_zip.__version__
purge()
sys.path.remove(WHEEL_PATH)

projects_after = sorted(os.listdir(SCRIPT_DIR))

check("the console script exits zero", ran.returncode == 0)
check("the console script prints the greeting",
      ran.stdout.strip() == "bookshop says hello")
check("the console script printed nothing to stderr", not ran.stderr.strip())
check("without its folder it cannot find the package", ran_alone.returncode != 0)
check("the wheel imports with nothing installed", zip_imported)
check("the wheel still knows its version", zip_version == VERSION)
check("this folder is untouched", projects_before == projects_after)
check("no file was left in the projects folder",
      projects_before == projects_after)

print("T10  the console script ran and exited ->", ran.returncode)
print("T10  and printed ->", ran.stdout.strip())
print("T10  the same script with no folder on the path ->",
      ran_alone.returncode)
print("T10  because --target is a folder, not an environment ->",
      ran_alone.returncode != 0)
print("T10  the wheel still imports straight from the zip ->", zip_imported)
print("T10  and the folder this file lives in is untouched ->",
      projects_before == projects_after)
print()

# ------------------------------------------------------------
# clean up and report
# ------------------------------------------------------------
purge()
for path in (WHEEL_PATH, TAMPERED_PATH):
    if os.path.exists(path):
        os.remove(path)
shutil.rmtree(FOLDER, ignore_errors=True)

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
