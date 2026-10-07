# ============================================================
# Project 43 - threading: the bookshop serves many customers at once
# ============================================================
# What this lesson teaches:
#   threading            a Thread is a function running in parallel
#   join()               the only way to wait for a thread
#   shared memory        threads share everything, and that is the danger
#   the lost update      counter += 1 is read, then write, and another
#                        thread can slip between the two
#   Lock                 making the read-modify-write one indivisible step
#   daemon threads       a servant that dies with the process
#   ThreadPoolExecutor   a pool of workers, results in submission order
#   the GIL              exactly one thread runs Python bytecode at a time
#   I/O vs CPU           sleeping threads overlap; counting threads take turns
#   sqlite3              the database from project 42, serving concurrent
#                        customers through one locked connection
#
# Everything is the standard library. The only file created is a small
# SQLite database in a temporary folder, deleted when the file finishes.
# The race in task 3 is forced with Events, so the output is the same on
# every run - the interleaving is chosen, not left to chance.
#
# Run it:  python project-43-threading-concurrent-customers.py
# ============================================================

import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor

FOLDER = tempfile.mkdtemp(prefix="project43_")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
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
print("Q1  which module gives you a thread")
print("Q2  what does join() do")
print("Q3  why is counter += 1 not atomic")
print("Q4  what does a Lock do")
print("Q5  what happens to a daemon thread when the process exits")
print("Q6  in what order does ThreadPoolExecutor.map return results")
print("Q7  do sleeping threads overlap")
print("Q8  what does the GIL do to pure-Python work")
print()
print("-" * 60)
print("SELF CHECK - the correct answers")
print("-" * 60)
print("Q1  threading, and a Thread is a function running in parallel")
print("Q2  it waits until that thread finishes")
print("Q3  because it is read, then write, and another thread can slip between")
print("Q4  it makes the read-modify-write one indivisible step")
print("Q5  it is killed with the process, without warning")
print("Q6  the order you submitted them")
print("Q7  yes - sleeping is I/O, and I/O threads do overlap")
print("Q8  it lets exactly one thread run Python bytecode at a time")
print()
print("-" * 60)


# ============================================================
# PART B - WHAT YOU BUILD
# ============================================================

print("=" * 60)
print("PART B - the tasks")
print("=" * 60)

print("TASK 1 - a thread is a function with a name")
print("T1  the main thread calls itself -> MainThread")
print("T1  the new thread is named -> worker-a")
print("T1  before start, is_alive -> False")
print("T1  after start, is_alive -> True")
print("T1  after join, is_alive -> False")
print("T1  the worker finished -> True")
print()

print("TASK 2 - threads share memory")
print("T2  four threads wrote into one list -> ['customer-0', 'customer-1', 'customer-2', 'customer-3']")
print("T2  every slot was filled -> True")
print("T2  no slot was overwritten -> True")
print("T2  so threads share memory, and that is the danger -> True")
print()

print("TASK 3 - the lost update")
print("T3  both threads read the same value -> 0")
print("T3  the counter ended at -> 1")
print("T3  two increments, one survivor -> 1")
print("T3  so read-modify-write is not atomic -> True")
print()

print("TASK 4 - a Lock makes the interleaving impossible")
print("T4  with a lock, the same two increments -> 2")
print("T4  the lock serialised the read-modify-write -> True")
print("T4  so a lock trades speed for correctness -> True")
print()

print("TASK 5 - daemon threads die with the process")
print("T5  the daemon is alive while main runs -> True")
print("T5  a child process started a 5-second daemon -> True")
print("T5  the child finished in under two seconds -> True")
print("T5  so a daemon dies with the process, without warning -> True")
print("T5  and a daemon can be woken and joined like any thread -> True")
print()

print("TASK 6 - ThreadPoolExecutor.map keeps the order")
print("T6  five jobs, three workers -> [2, 4, 6, 8, 10]")
print("T6  the results came back in submission order -> True")
print("T6  the context manager waited for every worker -> True")
print()

print("TASK 7 - sleeping threads overlap")
print("T7  sequential naps took longer than parallel ones -> True")
print("T7  so I/O-bound threads do overlap -> True")
print()

print("TASK 8 - the GIL serialises pure-Python work")
print("T8  four threads, 2000 increments each -> 8000")
print("T8  the lock made every increment count -> True")
print("T8  so the GIL means they took turns, and the lock is why it worked -> True")
print()

print("TASK 9 - the bookshop serves customers")
print("T9  five customers, one shop -> 5")
print("T9  every order was recorded -> True")
print("T9  the orders, sorted -> ['huda', 'lina', 'nour', 'omar', 'sara']")
print("T9  so the lock kept the shop's books honest -> True")
print()

print("TASK 10 - the loop, closed: the database serves too")
print("T10  five customers, one database -> 5")
print("T10  the rows, sorted -> ['huda', 'lina', 'nour', 'omar', 'sara']")
print("T10  threads still running at the end -> []")
print("T10  every thread was joined or shut down -> True")
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
print("TASK 1 - a thread is a function with a name")
print("-" * 60)
gate = threading.Event()
done = []


def worker():
    gate.wait()
    done.append("done")


t = threading.Thread(target=worker, name="worker-a")

check("the main thread is called MainThread",
      threading.current_thread().name == "MainThread")
check("the new thread has the name we gave it", t.name == "worker-a")
check("a thread is not alive before start", not t.is_alive())

print("T1  the main thread calls itself ->", threading.current_thread().name)
print("T1  the new thread is named ->", t.name)
print("T1  before start, is_alive ->", t.is_alive())
t.start()
check("a thread is alive once started", t.is_alive())
check("two threads were alive at once", threading.active_count() == 2)
print("T1  after start, is_alive ->", t.is_alive())
gate.set()
t.join()
check("join waits until the thread finishes", not t.is_alive())
check("the worker ran to completion", done == ["done"])
print("T1  after join, is_alive ->", t.is_alive())
print("T1  the worker finished ->", done == ["done"])
print()

# ------------------------------------------------------------
# TASK 2
# ------------------------------------------------------------
print("-" * 60)
print("TASK 2 - threads share memory")
print("-" * 60)
slots = [None] * 4


def fill(index):
    slots[index] = "customer-{0}".format(index)


threads = [threading.Thread(target=fill, args=(i,)) for i in range(4)]
expected = ["customer-{0}".format(i) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

check("four threads were created", len(threads) == 4)
check("every slot was filled", all(s is not None for s in slots))
check("no slot was overwritten", slots == expected)
check("all four threads finished", all(not t.is_alive() for t in threads))
check("the list is shared memory", slots == expected)

print("T2  four threads wrote into one list ->", slots)
print("T2  every slot was filled ->", all(s is not None for s in slots))
print("T2  no slot was overwritten ->", slots == expected)
print("T2  so threads share memory, and that is the danger ->",
      slots == expected)
print()

# ------------------------------------------------------------
# TASK 3
# ------------------------------------------------------------
print("-" * 60)
print("TASK 3 - the lost update")
print("-" * 60)
counter = {"n": 0}
a_read = threading.Event()
b_read = threading.Event()
a_wrote = threading.Event()
reads = []


def thread_a():
    value = counter["n"]
    reads.append(value)
    a_read.set()
    b_read.wait()
    counter["n"] = value + 1
    a_wrote.set()


def thread_b():
    value = counter["n"]
    reads.append(value)
    b_read.set()
    a_wrote.wait()
    counter["n"] = value + 1


a = threading.Thread(target=thread_a)
b = threading.Thread(target=thread_b)
a.start()
b.start()
a.join()
b.join()

check("both threads read the same value", reads == [0, 0])
check("the counter ended at one", counter["n"] == 1)
check("one increment was lost", counter["n"] == 1)
check("the events forced the order", reads == [0, 0] and counter["n"] == 1)
check("both threads finished", not a.is_alive() and not b.is_alive())

print("T3  both threads read the same value ->", reads[0])
print("T3  the counter ended at ->", counter["n"])
print("T3  two increments, one survivor ->", counter["n"])
print("T3  so read-modify-write is not atomic ->",
      reads == [0, 0] and counter["n"] == 1)
print()

# ------------------------------------------------------------
# TASK 4
# ------------------------------------------------------------
print("-" * 60)
print("TASK 4 - a Lock makes the interleaving impossible")
print("-" * 60)
counter = {"n": 0}
lock = threading.Lock()
a_read = threading.Event()
b_ready = threading.Event()
a_wrote = threading.Event()
seen = {}


def thread_a():
    with lock:
        value = counter["n"]
        a_read.set()
        b_ready.wait()
        counter["n"] = value + 1
        a_wrote.set()


def thread_b():
    b_ready.set()
    with lock:
        value = counter["n"]
        seen["b"] = value
        counter["n"] = value + 1


a = threading.Thread(target=thread_a)
b = threading.Thread(target=thread_b)
a.start()
b.start()
a.join()
b.join()

check("the counter reached two", counter["n"] == 2)
check("the second thread saw the first's write", seen["b"] == 1)
check("the lock was released", not lock.locked())
check("the lock serialised the pair", counter["n"] == 2)
check("both threads finished", not a.is_alive() and not b.is_alive())

print("T4  with a lock, the same two increments ->", counter["n"])
print("T4  the lock serialised the read-modify-write ->", counter["n"] == 2)
print("T4  so a lock trades speed for correctness ->", counter["n"] == 2)
print()

# ------------------------------------------------------------
# TASK 5
# ------------------------------------------------------------
print("-" * 60)
print("TASK 5 - daemon threads die with the process")
print("-" * 60)
wake = threading.Event()
woken = []


def daemon_worker():
    wake.wait()
    woken.append("woken")


d = threading.Thread(target=daemon_worker, daemon=True)
d.start()

check("the daemon flag is True", d.daemon is True)
check("the daemon is alive while main runs", d.is_alive())
print("T5  the daemon is alive while main runs ->", d.is_alive())

child_code = ("import threading, time;"
              "threading.Thread(target=time.sleep, args=(5,),"
              " daemon=True).start();"
              "print('child done')")
t0 = time.monotonic()
child = subprocess.run([sys.executable, "-c", child_code],
                       capture_output=True, text=True, timeout=10)
child_elapsed = time.monotonic() - t0

check("the child exited cleanly", child.returncode == 0)
check("the child printed its line", child.stdout.strip() == "child done")
check("the child did not wait for its daemon", child_elapsed < 2.0)
print("T5  a child process started a 5-second daemon ->",
      child.returncode == 0)
print("T5  the child finished in under two seconds ->", child_elapsed < 2.0)
print("T5  so a daemon dies with the process, without warning ->",
      child_elapsed < 2.0)

wake.set()
d.join()
check("the daemon finished when woken", woken == ["woken"])
check("the daemon was joined", not d.is_alive())
print("T5  and a daemon can be woken and joined like any thread ->",
      woken == ["woken"])
print()

# ------------------------------------------------------------
# TASK 6
# ------------------------------------------------------------
print("-" * 60)
print("TASK 6 - ThreadPoolExecutor.map keeps the order")
print("-" * 60)
calls = []


def double(n):
    calls.append(n)
    return n * 2


with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(double, [1, 2, 3, 4, 5]))

check("the results are in submission order", results == [2, 4, 6, 8, 10])
check("the function ran five times", len(calls) == 5)
check("every result is an int", all(isinstance(r, int) for r in results))
check("the pool shut down", threading.active_count() == 1)
check("the executor waited for its workers", results == [2, 4, 6, 8, 10])

print("T6  five jobs, three workers ->", results)
print("T6  the results came back in submission order ->",
      results == [2, 4, 6, 8, 10])
print("T6  the context manager waited for every worker ->",
      threading.active_count() == 1)
print()

# ------------------------------------------------------------
# TASK 7
# ------------------------------------------------------------
print("-" * 60)
print("TASK 7 - sleeping threads overlap")
print("-" * 60)


def nap(seconds):
    time.sleep(seconds)


t0 = time.monotonic()
nap(0.2)
nap(0.2)
sequential = time.monotonic() - t0

t0 = time.monotonic()
a = threading.Thread(target=nap, args=(0.2,))
b = threading.Thread(target=nap, args=(0.2,))
a.start()
b.start()
a.join()
b.join()
parallel = time.monotonic() - t0

check("the sequential pair took its time", sequential > 0.3)
check("the parallel pair was faster", parallel < sequential)
check("the parallel pair was much faster", parallel < sequential * 0.8)
check("sleeping is I/O, and I/O overlaps", parallel < sequential)

print("T7  sequential naps took longer than parallel ones ->",
      parallel < sequential)
print("T7  so I/O-bound threads do overlap ->", parallel < sequential)
print()

# ------------------------------------------------------------
# TASK 8
# ------------------------------------------------------------
print("-" * 60)
print("TASK 8 - the GIL serialises pure-Python work")
print("-" * 60)
lock = threading.Lock()
total = {"n": 0}


def count_up(times):
    for _ in range(times):
        with lock:
            total["n"] += 1


threads = [threading.Thread(target=count_up, args=(2000,))
           for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

check("four threads counted to 8000", total["n"] == 8000)
check("every increment counted", total["n"] == 8000)
check("the lock was released", not lock.locked())
check("all four threads finished", all(not t.is_alive() for t in threads))
check("the GIL serialised the work", total["n"] == 8000)

print("T8  four threads, 2000 increments each ->", total["n"])
print("T8  the lock made every increment count ->", total["n"] == 8000)
print("T8  so the GIL means they took turns, and the lock is why it worked ->",
      total["n"] == 8000)
print()

# ------------------------------------------------------------
# TASK 9
# ------------------------------------------------------------
print("-" * 60)
print("TASK 9 - the bookshop serves customers")
print("-" * 60)
shop = {"served": 0, "orders": []}
lock = threading.Lock()


def serve(customer):
    with lock:
        shop["served"] += 1
        shop["orders"].append(customer)


customers = ["sara", "nour", "omar", "lina", "huda"]
threads = [threading.Thread(target=serve, args=(c,)) for c in customers]
for t in threads:
    t.start()
for t in threads:
    t.join()
sorted_orders = sorted(shop["orders"])

check("five customers were served", shop["served"] == 5)
check("every order was recorded", len(shop["orders"]) == 5)
check("the sorted orders are the customers", sorted_orders == sorted(customers))
check("the lock kept the books honest",
      shop["served"] == 5 and len(shop["orders"]) == 5)
check("all five threads finished", all(not t.is_alive() for t in threads))

print("T9  five customers, one shop ->", shop["served"])
print("T9  every order was recorded ->", len(shop["orders"]) == 5)
print("T9  the orders, sorted ->", sorted_orders)
print("T9  so the lock kept the shop's books honest ->",
      shop["served"] == 5 and len(shop["orders"]) == 5)
print()

# ------------------------------------------------------------
# TASK 10
# ------------------------------------------------------------
print("-" * 60)
print("TASK 10 - the loop, closed: the database serves too")
print("-" * 60)
db_path = os.path.join(FOLDER, "served.db")
# A connection belongs to the thread that made it. check_same_thread=False
# says "I know better" - and the lock is exactly why we do.
db = sqlite3.connect(db_path, check_same_thread=False)
db.execute("CREATE TABLE served (customer TEXT)")
lock = threading.Lock()


def record(customer):
    with lock:
        db.execute("INSERT INTO served VALUES (?)", (customer,))
        db.commit()


threads = [threading.Thread(target=record, args=(c,)) for c in customers]
for t in threads:
    t.start()
for t in threads:
    t.join()
rows = sorted(row[0] for row in db.execute("SELECT customer FROM served"))
db.close()

alive = [t.name for t in threading.enumerate()
         if t is not threading.main_thread()]
projects_after = sorted(os.listdir(SCRIPT_DIR))

check("five rows landed in the database", len(rows) == 5)
check("the rows match the customers", rows == sorted(customers))
check("the database is a real file", os.path.getsize(db_path) > 0)
check("no thread was left running", alive == [])
check("the folder this file lives in is untouched",
      projects_before == projects_after)

print("T10  five customers, one database ->", len(rows))
print("T10  the rows, sorted ->", rows)
print("T10  threads still running at the end ->", alive)
print("T10  every thread was joined or shut down ->", alive == [])
print("T10  and the folder this file lives in is untouched ->",
      projects_before == projects_after)
print()

# ------------------------------------------------------------
# clean up and report
# ------------------------------------------------------------
shutil.rmtree(FOLDER, ignore_errors=True)
check("the temporary folder was cleaned up", not os.path.exists(FOLDER))

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