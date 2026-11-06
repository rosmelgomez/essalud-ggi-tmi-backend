"""Variables del TMI dinámico: tmi_variable, sus componentes (variables compuestas) y su lógica."""

import logging

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DIM
from src.main.repositories.tmiBaseRep import (
    name_server,
    _consulta,
    queryInsertarFila,
    queryActualizarFila,
    queryEliminarFila,
)
from src.main.repositories.indicadorRep import queryGuardarFormulaTMI

logger = logging.getLogger(__name__)


def queryVariablesTMI(db: Session):
    return _consulta(db, f"""
        SELECT v.id, v.nombre, v.descripcion, v.agregacion, v.total_anual, v.activo,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_logica l WHERE l.id_variable = v.id) AS filas_logica,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_componente c WHERE c.id_variable = v.id) AS componentes
        FROM {name_server}.tmi_variable v
        ORDER BY v.nombre""")


def queryActualizarVariableTMI(db: Session, id: int, datos: dict, usuario: str = None):
    """Actualiza la variable si su nuevo cálculo coincide con el de las variables que suma y las que la suman."""
    distintas = _consulta(db, f"""
        SELECT v.nombre FROM {name_server}.tmi_variable_componente c
        JOIN {name_server}.tmi_variable v ON v.id = CASE WHEN c.id_variable = :id THEN c.id_variable_componente ELSE c.id_variable END
        WHERE (c.id_variable = :id OR c.id_variable_componente = :id) AND v.agregacion <> :agregacion""",
        {"id": id, "agregacion": datos["agregacion"]})
    if distintas:
        raise HTTPException(status_code=400, detail=f"No se puede cambiar el cálculo a {datos['agregacion']}: la variable suma "
                            "o es sumada por variables con otro cálculo: " + ", ".join(sorted(d["nombre"] for d in distintas)))
    return queryActualizarFila(db, "tmi_variable", id, datos, usuario)


def queryEliminarVariable(db: Session, id: int):
    usada = _consulta(db, f"""
        SELECT DISTINCT i.codigo FROM {name_server}.tmi_indicador_variable iv
        JOIN {name_server}.tmi_indicador i ON i.id = iv.id_indicador WHERE iv.id_variable = :id""", {"id": id})
    if usada:
        raise HTTPException(status_code=400, detail="La variable se usa en los indicadores: "
                            + ", ".join(sorted(u["codigo"] or "" for u in usada)))
    padres = _consulta(db, f"""
        SELECT v.nombre FROM {name_server}.tmi_variable_componente c
        JOIN {name_server}.tmi_variable v ON v.id = c.id_variable WHERE c.id_variable_componente = :id""", {"id": id})
    if padres:
        raise HTTPException(status_code=400, detail="La variable es componente de: "
                            + ", ".join(sorted(p["nombre"] for p in padres)))
    try:
        db.execute(text(f"DELETE FROM {name_server}.tmi_variable_logica WHERE id_variable = :id"), {"id": id})
        db.execute(text(f"DELETE FROM {name_server}.tmi_variable_componente WHERE id_variable = :id"), {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return queryEliminarFila(db, "tmi_variable", id)


def queryVariableComponentesTMI(db: Session, id_variable: int):
    """Componentes de una variable compuesta, con lo que suma cada uno."""
    return _consulta(db, f"""
        SELECT c.id, c.id_variable, c.id_variable_componente, c.activo, v.nombre AS componente, v.activo AS componente_activo,
               v.agregacion,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_logica l WHERE l.id_variable = v.id AND l.activo = 1) AS filas_logica,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_componente c2 WHERE c2.id_variable = v.id) AS componentes
        FROM {name_server}.tmi_variable_componente c
        JOIN {name_server}.tmi_variable v ON v.id = c.id_variable_componente
        WHERE c.id_variable = :id
        ORDER BY v.nombre""", {"id": id_variable})


def queryInsertarComponenteTMI(db: Session, datos: dict):
    """Agrega un componente si no forma un ciclo (la variable no puede contenerse a sí misma)."""
    ciclo = db.execute(text(f"""
        ;WITH arbol AS (
            SELECT :comp AS id_var, 0 AS nivel
            UNION ALL
            SELECT c.id_variable_componente, a.nivel + 1
            FROM arbol a JOIN {name_server}.tmi_variable_componente c ON c.id_variable = a.id_var AND c.activo = 1
            WHERE a.nivel < 10)
        SELECT COUNT(*) FROM arbol WHERE id_var = :var OPTION (MAXRECURSION 20)"""),
        {"comp": datos["id_variable_componente"], "var": datos["id_variable"]}).scalar()
    if datos["id_variable"] == datos["id_variable_componente"] or ciclo:
        raise HTTPException(status_code=400, detail="Ese componente contiene a la variable: se formaría un ciclo.")
    calculos = db.execute(text(f"""
        SELECT COUNT(DISTINCT agregacion) FROM {name_server}.tmi_variable WHERE id IN (:var, :comp)"""),
        {"comp": datos["id_variable_componente"], "var": datos["id_variable"]}).scalar()
    if calculos > 1:
        raise HTTPException(status_code=400, detail="La variable y el componente tienen distinto cálculo (SUMA y MEDIANA): "
                                                    "no se pueden sumar.")
    return queryInsertarFila(db, "tmi_variable_componente", datos)


def queryVariableLogicaTMI(db: Session, id_variable: int):
    return _consulta(db, f"""
        SELECT l.id, l.id_variable, l.tipgrupo, l.actividad, l.servicio, l.condicion_hoja,
               l.periodo_desde, l.periodo_hasta, l.activo, g.desctipgrupo,
               a.descactividad AS descactividad_corta, a.desclarga, a.Recurso, a.Proceso,
               COALESCE(NULLIF(LTRIM(RTRIM(a.desclarga)), ''), a.descactividad) AS descactividad
        FROM {name_server}.tmi_variable_logica l
        LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = l.tipgrupo
        LEFT JOIN {TMI_DIM}.DIM_ACTIVIDAD a ON a.actividad = l.actividad
        WHERE l.id_variable = :id
        ORDER BY l.tipgrupo, l.actividad, l.servicio""", {"id": id_variable})


def queryVariableDeFila(db: Session, tabla: str, id: int):
    """Variable dueña de una fila de lógica o de componente (para regenerar fórmulas después de borrarla)."""
    if tabla not in ("tmi_variable_logica", "tmi_variable_componente"):
        raise ValueError(tabla)
    return db.execute(text(f"SELECT id_variable FROM {name_server}.{tabla} WHERE id = :id"), {"id": id}).scalar()


def regenerarFormulasVariable(db: Session, id_variable: int) -> None:
    """Una variable cambió (conjuntos, componentes o cálculo): se vuelve a generar la fórmula interna de los indicadores
    que la usan, directo o dentro de una variable compuesta. Si no se puede (p. ej. quedó sin conjuntos), el indicador
    conserva su fórmula anterior y se avisa en el log."""
    try:
        ids = [r[0] for r in db.execute(text(f"""
            WITH arriba AS (
                SELECT CAST(:id AS INT) AS id_var, 0 AS nivel
                UNION ALL
                SELECT c.id_variable, a.nivel + 1
                FROM arriba a JOIN {name_server}.tmi_variable_componente c ON c.id_variable_componente = a.id_var
                WHERE a.nivel < 10
            )
            SELECT DISTINCT iv.id_indicador
            FROM {name_server}.tmi_indicador_variable iv
            JOIN {name_server}.tmi_indicador i ON i.id = iv.id_indicador AND i.formula_alias IS NOT NULL
            WHERE iv.id_variable IN (SELECT id_var FROM arriba)
            OPTION (MAXRECURSION 20)"""), {"id": id_variable}).all()]
    except Exception as e:
        db.rollback()
        logger.warning("No se pudo buscar los indicadores de la variable %s: %s", id_variable, e)
        return
    for id_ind in ids:
        try:
            alias = db.execute(text(f"SELECT formula_alias FROM {name_server}.tmi_indicador WHERE id = :id"),
                               {"id": id_ind}).scalar()
            letras = {r[0]: r[1] for r in db.execute(text(f"""SELECT letra, id_variable FROM {name_server}.tmi_indicador_variable
                                                             WHERE id_indicador = :id"""), {"id": id_ind}).all()}
            queryGuardarFormulaTMI(db, id_ind, alias, letras, "sistema")
        except Exception as e:
            db.rollback()
            logger.warning("No se pudo regenerar la fórmula del indicador %s: %s", id_ind, getattr(e, "detail", e))
