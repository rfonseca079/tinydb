import sys, time, importlib, statistics
import os; sys.path.insert(0, os.getcwd())
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

def make(n):
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple([{'n': i, 'tags': ['a', 'b'], 'meta': {'k': i}} for i in range(n)])
    return db

def timeit(fn, reps=7):
    ts = []
    for _ in range(reps):
        t = time.perf_counter(); fn(); ts.append(time.perf_counter() - t)
    return statistics.median(ts) * 1000

def inc(d): d['n'] += 1

for n in (1000, 10000):
    db = make(n)
    r_upd1 = timeit(lambda: db.update(inc, doc_ids=[1]))
    r_updall = timeit(lambda: db.update(inc))
    r_ins = timeit(lambda: db.insert({'n': -1}))
    r_rem = timeit(lambda: db.remove(doc_ids=[1]))
    print(f"N={n:>6} | update 1 doc: {r_upd1:8.3f} ms | update todos: {r_updall:9.3f} ms | insert: {r_ins:8.3f} ms | remove 1: {r_rem:8.3f} ms")
