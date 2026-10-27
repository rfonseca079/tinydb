"""Mide el costo de la corrección de HU-3 (update sobre una copia del documento).

Uso:

    py scripts/bench_hu3.py [ruta_del_repositorio]

Crea una base en memoria con 1 000 y 10 000 documentos y mide, con
time.perf_counter, la mediana de 7 repeticiones de cuatro operaciones.

Sin argumento evalúa este repositorio. Para medir el código previo a HU-3,
crear una copia de trabajo en ese commit y pasar su ruta:

    git worktree add ../tinydb-antes aa4a09f
    py scripts/bench_hu3.py ../tinydb-antes
"""
import statistics
import sys
import time
from pathlib import Path



def ruta_repositorio():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return Path(__file__).resolve().parent.parent


RUTA = ruta_repositorio()
sys.path.insert(0, str(RUTA))

from tinydb import TinyDB  # noqa: E402
from tinydb.storages import MemoryStorage  # noqa: E402

REPETICIONES = 7
TAMANOS = (1000, 10000)


def crear_base(n):
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple(
        [{'n': i, 'tags': ['a', 'b'], 'meta': {'k': i}} for i in range(n)]
    )
    return db


def mediana_ms(operacion):
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        operacion()
        tiempos.append(time.perf_counter() - inicio)
    return statistics.median(tiempos) * 1000


def incrementar(doc):
    doc['n'] += 1


def medir(n):
    db = crear_base(n)
    return (
        mediana_ms(lambda: db.update(incrementar, doc_ids=[1])),
        mediana_ms(lambda: db.update(incrementar)),
        mediana_ms(lambda: db.insert({'n': -1})),
        mediana_ms(lambda: db.remove(doc_ids=[1])),
    )


if __name__ == '__main__':
    print('Repositorio evaluado:', RUTA)
    for tamano in TAMANOS:
        uno, todos, insertar, borrar = medir(tamano)
        print(
            f'N={tamano:>6} | update 1 doc: {uno:8.3f} ms | '
            f'update todos: {todos:9.3f} ms | insert: {insertar:8.3f} ms | '
            f'remove 1: {borrar:8.3f} ms'
        )
