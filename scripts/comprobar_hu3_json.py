"""Comprueba si un update() que falla a mitad deja cambios parciales (HU-3).

Ejecuta la misma actualización fallida con MemoryStorage y con JSONStorage e
indica si la base quedó con cambios parciales.

Uso:

    py scripts/comprobar_hu3_json.py [ruta_del_repositorio]

Sin argumento evalúa este repositorio. Para evaluar el código previo a HU-3,
crear una copia de trabajo en ese commit y pasar su ruta:

    git worktree add ../tinydb-antes aa4a09f
    py scripts/comprobar_hu3_json.py ../tinydb-antes
"""
import contextlib
import sys
import tempfile
from pathlib import Path


def ruta_repositorio():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return Path(__file__).resolve().parent.parent


RUTA = ruta_repositorio()
sys.path.insert(0, str(RUTA))

from tinydb import TinyDB  # noqa: E402
from tinydb.storages import MemoryStorage  # noqa: E402


def falla_en_tercero(doc):
    if doc['n'] == 3:
        raise RuntimeError('fallo simulado')
    doc['n'] += 10


def probar(nombre, db):
    db.insert_multiple([{'n': 1}, {'n': 2}, {'n': 3}])
    antes = db.all()
    with contextlib.suppress(RuntimeError):
        db.update(falla_en_tercero)
    despues = db.all()
    estado = 'SIN cambios parciales' if despues == antes else 'CON cambios parciales'
    print(f'{nombre:<14} antes={antes}  despues={despues}  -> {estado}')


if __name__ == '__main__':
    print('Repositorio evaluado:', RUTA)
    probar('MemoryStorage', TinyDB(storage=MemoryStorage))
    ruta_json = Path(tempfile.mkdtemp()) / 'db.json'
    probar('JSONStorage', TinyDB(str(ruta_json)))
