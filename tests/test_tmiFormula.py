"""Fórmula del indicador: parser, regla de nulos y SQL que genera (sin base de datos)."""

import pytest

from src.main.core import tmiFormula as F

FORMULA = "[1;3] / [1;1]"


@pytest.mark.parametrize("letra, division, esperado", [
    ("CERO", "NA", "ISNULL(p.[T1],0) / NULLIF(ISNULL(p.[T2],0),0)"),          # por defecto (como 00_TMI_CREACION_VISTAS)
    ("NA", "NA", "p.[T1] / NULLIF(p.[T2],0)"),
    ("CERO", "CERO", "ISNULL((ISNULL(p.[T1],0)) / NULLIF(ISNULL(p.[T2],0),0), 0)"),
    ("NA", "CERO", "ISNULL((p.[T1]) / NULLIF(p.[T2],0), 0 * (p.[T1]) * (p.[T2]))"),
])
def test_regla_de_nulos(letra, division, esperado):
    assert F.analizar(FORMULA, letra, division).sql == esperado


def test_regla_por_defecto_es_cero_y_na():
    assert F.analizar(FORMULA).sql == F.analizar(FORMULA, "CERO", "NA").sql


def test_mediana_y_numeros():
    f = F.analizar("MEDIANA([5;7#3]) + 2*[1;1]")
    assert f.sql == "ISNULL(p.[T1],0) + 2.0 * ISNULL(p.[T2],0)"
    assert f.terminos[0].mediana and 3 in f.terminos[0].servicios


def test_termino_repetido_es_una_sola_columna():
    assert F.analizar("[1;3] + [1;3]").sql == "ISNULL(p.[T1],0) + ISNULL(p.[T1],0)"


@pytest.mark.parametrize("texto", [
    "", "[1;3] /", "([1;3]", "2 + 3", "[1;3] ; DROP TABLE x", "[1;3] -- comentario", "x" * 2001,
])
def test_formulas_invalidas(texto):
    with pytest.raises(F.ErrorFormula):
        F.analizar(texto)


def test_regla_de_nulos_invalida():
    with pytest.raises(F.ErrorFormula):
        F.analizar(FORMULA, "OTRO", "NA")


def test_sql_solo_tiene_caracteres_permitidos():
    """Misma comprobación que usp_tmi_calcular antes de ejecutar formula_sql."""
    import re
    for regla in [("CERO", "NA"), ("NA", "NA"), ("CERO", "CERO"), ("NA", "CERO")]:
        sql = F.analizar("([1;3] - MEDIANA([5;7#3])) / ([1;1] * 100)", *regla).sql
        resto = sql
        for quitar in ("ISNULL(", "NULLIF(", "p.[T", "]"):
            resto = resto.replace(quitar, "")
        assert re.fullmatch(r"[-0-9 .,()+*/]*", resto), sql


def test_letras_y_alias():
    assert F.letras_usadas("(A - B) / C") == ["A", "B", "C"]
    assert F.expandir_alias("A / B", {"A": "[1;3]", "B": "[1;1]"}) == "[1;3] / [1;1]"
    with pytest.raises(F.ErrorFormula):
        F.expandir_alias("A / Z", {"A": "[1;3]"})


def test_consulta_sql_completa_usa_las_funciones_de_calcular():
    sql = F.consulta_sql(F.analizar(FORMULA), "x.dbo.TOTALIZADO3", "ACUMULADO", 202606, "IND",
                         centros="t.dbo.vw_tmi_centro_base", indicador={"id": 7, "base_estandar": "NIVEL"},
                         esquema="t.dbo")
    assert "t.dbo.fn_tmi_estandar(@PERIODO)" in sql and "t.dbo.fn_tmi_exclusion(@PERIODO)" in sql
    assert "DECLARE @ID_INDICADOR INT = 7;" in sql
    assert "[202601]" in sql and "[202612]" in sql and "HAVING MAX(es.estandar) IS NOT NULL" in sql


def test_consulta_sql_solo_formula_no_lee_estandares():
    sql = F.consulta_sql(F.analizar(FORMULA), "x.dbo.TOTALIZADO3", "MENSUAL", 202606, "IND",
                         centros="t.dbo.vw_tmi_centro_base")
    assert "fn_tmi_estandar" not in sql and "Estandar" not in sql
