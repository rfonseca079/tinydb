# Evidencia del incremento (HU-1 a HU-4)

Salidas de consola y capturas generadas durante el desarrollo dirigido por pruebas del incremento sobre TinyDB (equipo Foo, curso PSWE-06).

**Notas sobre los archivos**

- Para no exponer datos personales, las rutas locales de la computadora donde se ejecutaron los comandos se reemplazaron por `[ruta de los archivos]`. Se conservan la raíz (`C:\Users\`) y la carpeta relevante (`tinydb`, `Python313`, etc.). Es el único cambio al contenido original.
- Las coberturas de las ejecuciones con `-k` (pruebas de una sola historia) no son representativas. Solo se citan las de la suite completa (`*-suite.txt` y `cobertura-hu1.txt`), medidas con `.coverage` borrado.
- La línea base de Ruff (37 observaciones) está en `reports/ruff-baseline.txt`.

## Nombres de archivo

`hu<N>-<paso>-<descripción>`: el número de historia, el paso del ciclo y qué contiene.

| Paso | Contenido |
|---|---|
| 1 | Fase roja: pruebas de la historia fallando |
| 2 | Fase verde: pruebas de la historia pasando |
| 3 | Suite completa tras el cambio (con cobertura) |
| 4 | Diff del commit (`git show`) |
| 5 | Ruff sobre el archivo modificado |

## HU-1: `remove()` con identificadores repetidos

| Archivo | Qué muestra |
|---|---|
| `hu1-1-rojo.txt` | 2 pruebas fallan con `KeyError` (table.py, línea 659) |
| `hu1-2-verde.txt` | Las 2 pruebas pasan |
| `hu1-3-suite.txt` | 5 fallidas, 233 aprobadas (quedan HU-2, HU-3, HU-4) |
| `hu1-4-diff.txt` | Commit `6d6e292` |
| `hu1-5-ruff.txt` | 4 observaciones heredadas en `table.py` |
| `cobertura-hu1.txt` | Cobertura limpia: 95 % total, `middlewares.py` 100 % |

## HU-2: `update()` con identificadores repetidos

| Archivo | Qué muestra |
|---|---|
| `hu2-1-rojo.txt` | 2 pruebas fallan (`[1, 1, 2]`; `n = 3`) |
| `hu2-2-verde.txt` | Las 2 pruebas pasan |
| `hu2-3-suite.txt` | 3 fallidas, 235 aprobadas |
| `hu2-4-diff.txt` | Commit `e12d2a7` |
| `hu2-5-ruff.txt` | 4 observaciones (incluye C901) |
| `hu2-6-refactor-suite.txt` | Tras el refactor: mismo resultado, 3 fallidas, 235 aprobadas |
| `hu2-7-refactor-ruff.txt` | Tras el refactor: 3 observaciones, C901 eliminada |
| `hu2-8-refactor-diff.txt` | Commit `aa4a09f` |

## HU-4: cierre del middleware si falla `flush()`

| Archivo | Qué muestra |
|---|---|
| `hu4-1-rojo.txt` | 1 prueba falla, 2 pasan |
| `hu4-2-verde.txt` | Las 3 pasan |
| `hu4-3-suite.txt` | 2 fallidas, 236 aprobadas (queda HU-3) |
| `hu4-4-diff.txt` | Commit `de00fd2` |
| `hu4-5-ruff.txt` | 1 observación heredada en `middlewares.py` |

## HU-3: `update()` que falla a la mitad

| Archivo | Qué muestra |
|---|---|
| `hu3-0-bench-antes.txt` | Medición de desempeño antes de la corrección |
| `hu3-1-rojo.txt` | 2 pruebas fallan, 1 pasa |
| `hu3-2-verde.txt` | Las 3 pasan |
| `hu3-3-suite.txt` | 238 aprobadas, cobertura 95 % |
| `hu3-4-diff.txt` | Commit `59d28d9` |
| `hu3-5-ruff.txt` | 3 observaciones heredadas |
| `hu3-6-bench-despues.txt` | Medición de desempeño tras la corrección |
| `hu3-7-json-antes.txt` | Código previo a HU-3: `MemoryStorage` con cambios parciales, `JSONStorage` intacto |
| `hu3-8-json-despues.txt` | Código actual: ambos sin cambios parciales |

## Integración continua (GitHub Actions)

| Archivo | Qué muestra |
|---|---|
| `ci-run1-1-resumen.png`, `ci-run1-2-pasos-py314.png`, `ci-run1-3-log-py314.txt` | Ejecución #1 (commit `91ea67b`): 3 fallidas; los pasos de Ruff se ejecutan |
| `ci-run2-1-resumen.png`, `ci-run2-2-pasos-py314.png`, `ci-run2-3-log-py314.txt` | Ejecución #2 (commit `de00fd2`): 2 fallidas |
| `ci-run3-1-resumen.png`, `ci-run3-2-pasos-py314.png` | Ejecución #3 (commit `59d28d9`): todo en verde |

## Historial

`historial-final.txt`: salida de `git log --oneline` con los commits del equipo.

## Reproducir las mediciones

Los scripts están en `scripts/`. Sin argumento evalúan este repositorio; con una ruta, evalúan otra copia de trabajo, por ejemplo el commit previo a HU-3:

```
git worktree add ../tinydb-antes aa4a09f
py scripts/bench_hu3.py ../tinydb-antes
py scripts/comprobar_hu3_json.py ../tinydb-antes
git worktree remove ../tinydb-antes
```

Las mediciones `hu3-0-bench-antes.txt` y `hu3-6-bench-despues.txt` se obtuvieron con una versión previa de `bench_hu3.py`, con la misma lógica de medición; la versión del repositorio añade la ruta opcional. Las salidas `hu3-7-json-antes.txt` y `hu3-8-json-despues.txt` se obtuvieron con la primera versión de `comprobar_hu3_json.py`, ejecutada en un clon aparte (`tinydb-json`) situado en cada commit; la versión del repositorio añade la ruta opcional.
