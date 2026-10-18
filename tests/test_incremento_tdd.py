"""
Pruebas del incremento TDD (PSWE-06, equipo Foo).

Cada prueba referencia la historia de usuario (HU) que la origina.
"""
import pytest

from tinydb import TinyDB, where
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage, MemoryStorage


@pytest.fixture
def mem_db():
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple([{'n': 1}, {'n': 2}, {'n': 3}])
    yield db
    db.close()


# --- HU-1: remove(doc_ids=...) tolera IDs repetidos ------------------------

def test_hu1_remove_con_ids_repetidos_no_lanza_error(mem_db):
    removed = mem_db.remove(doc_ids=[1, 1])

    assert removed == [1]
    assert mem_db.all() == [{'n': 2}, {'n': 3}]


def test_hu1_remove_con_ids_repetidos_y_ausentes(mem_db):
    removed = mem_db.remove(doc_ids=[2, 2, 99, 2])

    assert removed == [2]
    assert [d.doc_id for d in mem_db.all()] == [1, 3]


# --- HU-2: update(doc_ids=...) aplica una sola vez por documento -----------

def test_hu2_update_con_ids_repetidos_devuelve_ids_unicos(mem_db):
    updated = mem_db.update({'n': 0}, doc_ids=[1, 1, 2])

    assert updated == [1, 2]


def test_hu2_update_callable_no_se_aplica_dos_veces(mem_db):
    def incrementar(doc):
        doc['n'] += 1

    mem_db.update(incrementar, doc_ids=[1, 1])

    assert mem_db.get(doc_id=1) == {'n': 2}  # 1 + 1, no 1 + 2


# --- HU-3: update/remove atomicos ante fallo a mitad de operacion ----------

def _falla_en_tercero(doc):
    if doc['n'] == 3:
        raise RuntimeError('fallo simulado')
    doc['n'] += 10


def test_hu3_update_con_callable_que_falla_no_deja_cambios_parciales(mem_db):
    antes = [dict(d) for d in mem_db.all()]

    with pytest.raises(RuntimeError):
        mem_db.update(_falla_en_tercero)

    assert mem_db.all() == antes


def test_hu3_update_por_condicion_con_callable_que_falla(mem_db):
    antes = [dict(d) for d in mem_db.all()]

    with pytest.raises(RuntimeError):
        mem_db.update(_falla_en_tercero, where('n') > 0)

    assert mem_db.all() == antes


def test_hu3_remove_con_condicion_que_falla_no_borra_parcialmente(mem_db):
    antes = [dict(d) for d in mem_db.all()]

    def condicion_defectuosa(doc):
        if doc['n'] == 3:
            raise RuntimeError('fallo simulado')
        return True

    with pytest.raises(RuntimeError):
        mem_db.remove(condicion_defectuosa)

    assert mem_db.all() == antes


# --- HU-4: CachingMiddleware.close() libera el archivo aunque falle --------

def test_hu4_close_libera_el_archivo_si_el_flush_falla(tmp_path):
    path = str(tmp_path / 'cache.json')
    db = TinyDB(path, storage=CachingMiddleware(JSONStorage))
    db.insert({'bad': {1, 2}})  # un set no es serializable a JSON

    with pytest.raises(TypeError):
        db.close()

    assert db._storage.storage._handle.closed
    assert db._storage._closed


def test_hu4_write_y_flush_tras_cierre_son_rechazados(tmp_path):
    storage = CachingMiddleware(MemoryStorage)
    storage()
    storage.close()

    with pytest.raises(ValueError, match='closed'):
        storage.write({})
    with pytest.raises(ValueError, match='closed'):
        storage.flush()


def test_hu4_close_es_idempotente():
    storage = CachingMiddleware(MemoryStorage)
    storage()
    storage.close()

    storage.close()  # no debe lanzar excepcion
