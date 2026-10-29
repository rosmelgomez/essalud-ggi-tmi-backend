
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de scripts SQLServer para metas/tarifas (versión Python con FRM)
- Replica la macro de Excel y añade lógica FRM automática.
- Si una expresión (col J) mezcla más de un par (grupo,actividad), usa FRM:
    * COD_GRUPO = 0, DESC_GRUPO = 'FRM'
    * COD_ACTI_SES = 0, DESC_ACT_SES = 'FRM'
  con GROUP BY ajustado a esos literales para evitar duplicados al desagregar.
- Si hay un único par (grupo,actividad), mantiene los campos originales.
- Consolida WHERE por (grupo;actividad) uniendo listas de servicio y respetando "sin servicio".
- Marca "compuesto" en col L si la expresión tiene + o -.
- Marca "FRM" en col M cuando se aplica FRM.
- Puede escribir nuevamente al Excel y además generar un archivo .sql consolidado.

Uso:
    python generador_sql_metas_FRM.py --input ruta.xlsx --inplace --sql-out salida.sql
Opcionales:
    --sheet "Generador de PLSQL (2)" --first-row 6 --last-row 314
    --expr-col 10 --sql-col 11 --flag-col 12 --frm-col 13 --desc-col 2
    --output ruta_salida.xlsx   (si no usas --inplace)
    --periodo-i 202401 --periodo-f 202412   (para predefinir DECLARE en el .sql)
"""

import argparse
from collections import defaultdict, OrderedDict
import re
from typing import List, Tuple, Dict, Optional
from openpyxl import load_workbook
from openpyxl.workbook.workbook import Workbook

# -------------------- Utilitarios de parsing --------------------

def normalize_expression(s: str) -> str:
    if s is None:
        return ""
    t = str(s)
    # quita espacios y () [] 
    for ch in [" ", "[", "]", "(", ")"]:
        t = t.replace(ch, "")
    return t.strip()

def is_composite_expression(s: str) -> bool:
    t = normalize_expression(s)
    return ("+" in t) or ("-" in t)

def parse_expression(expr: str) -> Tuple[List[str], List[int]]:
    """
    Divide la expresión en términos y signos (+1/-1).
    token esperado por término: g;a#s (donde s puede ser 0 o lista separada por coma)
    """
    expr = normalize_expression(expr)
    if not expr:
        return [], []

    terms: List[str] = []
    signs: List[int] = []
    token = ""
    sign = 1

    for c in expr:
        if c == "+":
            if token.strip():
                terms.append(token.strip()); signs.append(sign)
            token = ""; sign = 1
        elif c == "-":
            if token.strip():
                terms.append(token.strip()); signs.append(sign)
            token = ""; sign = -1
        else:
            token += c

    if token.strip():
        terms.append(token.strip()); signs.append(sign)

    return terms, signs

def parse_term(token: str) -> Optional[Tuple[int, int, str]]:
    """
    Devuelve (grupo, actividad, servicios_csv) o None si inválido.
    Formato: "g;a#s"  (s puede ser "0" o estar vacío para omitir filtro de servicio)
    """
    try:
        parts = token.split("#")
        ga = parts[0]
        g_str, a_str = ga.split(";")
        g = int(g_str); a = int(a_str)
        srv = ""
        if len(parts) >= 2:
            s = parts[1].strip()
            if s and s != "0":
                srv = s
        return (g, a, srv)
    except Exception:
        return None

# -------------------- Construcción de SQL --------------------

def merge_service_lists(a: str, b: str) -> str:
    if not a and not b:
        return ""
    if not a:
        return b
    if not b:
        return a
    seen = OrderedDict()
    for x in (a + "," + b).split(","):
        x = x.strip()
        if x:
            seen.setdefault(x, True)
    return ",".join(seen.keys())

def accumulate_where(d: Dict[Tuple[int,int], str], g: int, a: int, s: str):
    key = (g, a)
    if key not in d:
        d[key] = s or ""
    else:
        cur = d[key]
        if (not cur) or (not s):
            d[key] = ""  # si cualquiera es vacío => sin filtro servicio
        else:
            d[key] = merge_service_lists(cur, s)

def build_service_clause(services_csv: str) -> str:
    if services_csv:
        return f" AND servicio IN ({services_csv}) "
    return " "

def build_subquery(g: int, a: int, services_csv: str) -> str:
    srv = build_service_clause(services_csv)
    return (
        "(ISNULL((SELECT SUM(cantidad) FROM TOTALIZADO3 l,pentahodevDW.dbo.DIM_HOJA h WHERE "
        "l.tipohoja = h.tipohoja "
        f"AND tipgrupo={g} AND actividad={a}{srv}"
        "AND periodo = t.periodo "
        "AND codred_ses=T.codred_ses AND codcentro_ses=T.codcentro_ses),0))"
    )

def build_agg_with_signs(parts: List[str], signs: List[int]) -> str:
    sb = []
    if parts:
        # primer término
        if signs[0] < 0:
            sb.append("0 - ")
        sb.append(parts[0])
        # siguientes
        for i in range(1, len(parts)):
            sb.append(" + " if signs[i] >= 0 else " - ")
            sb.append(parts[i])
    agg = "".join(sb)
    return f"{agg} CANTIDAD,"

def build_where_block(where_map: Dict[Tuple[int,int], str]) -> str:
    if not where_map:
        return ""
    clauses = []
    for (g, a), s in where_map.items():
        if s:
            clauses.append(f"(tipgrupo={g} AND actividad={a} AND servicio IN ({s}))")
        else:
            clauses.append(f"(tipgrupo={g} AND actividad={a})")
    if len(clauses) == 1:
        return "and  " + clauses[0] + " "
    return "and  (" + " OR ".join(clauses) + ") "

def build_group_by(frm: bool) -> str:
    if not frm:
        return ("GROUP BY T.codred_ses,T.red_ses,T.codcentro_ses,tipgrupo,desctipgrupo,actividad,descactividad,"
                "c.desccentro_ses,c.nivel,T.periodo, T.nivel,T.descnivel ")
    # En FRM, agrupamos por literales 0 y 'FRM' para consolidar en una sola fila
    return ("GROUP BY T.codred_ses,T.red_ses,T.codcentro_ses,0,'FRM',0,'FRM',"
            "c.desccentro_ses,c.nivel,T.periodo, T.nivel,T.descnivel ")

def build_select_header(indice: int, descripcion_sql: str, frm: bool) -> str:
    common = (
        "SELECT T.codred_ses,T.red_ses,T.codcentro_ses, c.desccentro_ses , T.nivel COD_NIVEL, \n"
        "(SELECT DISTINCT NomMes FROM pentahodevDW.dbo.DIM_FECHA where mes = cast(RIGHT(T.periodo,2) as int)) MES, \n"
        f"LEFT(T.PERIODO,4) Año,"
    )
    if not frm:
        mid = "tipgrupo COD_GRUPO,desctipgrupo DESC_GRUPO,actividad COD_ACTI_SES,descactividad DESC_ACT_SES,"
    else:
        # Para mantener tipos consistentes: códigos numéricos a 0, descripciones como 'FRM'
        mid = "0 COD_GRUPO,'FRM' DESC_GRUPO,0 COD_ACTI_SES,'FRM' DESC_ACT_SES,"
    tail = f"{indice} COD_ACTIVIDAD, {descripcion_sql} DESCRIPCION_ACTIVIDAD, "
    return common + mid + tail

def build_from_where(where_block: str) -> str:
    return (
        "T.descnivel Nivel_Atencion \n"
        "FROM TOTALIZADO3 T, pentahodevDW.dbo.DIM_CENTRO c \n"
        "WHERE T.periodo BETWEEN @PERIODOI AND @PERIODOf and T.codcentro_ses=c.codcentro_ses \n"
        + where_block
    )

def build_sql_for_expression(raw_expr: str, descripcion: str, indice: int) -> Tuple[str, bool, bool]:
    """
    Devuelve (sql_fragment, is_composite, used_frm)
    - sql_fragment termina con 'Union All' (para concatenar luego)
    """
    expr = normalize_expression(raw_expr)
    if not expr:
        return "", False, False

    terms, signs = parse_expression(expr)
    if not terms:
        return "", False, False

    # Parsear términos válidos
    parts: List[str] = []
    where_map: Dict[Tuple[int,int], str] = OrderedDict()
    unique_pairs: List[Tuple[int,int]] = []

    for tkn in terms:
        parsed = parse_term(tkn)
        if not parsed:
            continue
        g, a, s = parsed
        parts.append(build_subquery(g, a, s))
        # acumular where y registrar par único
        if (g, a) not in where_map:
            unique_pairs.append((g, a))
        accumulate_where(where_map, g, a, s)

    if not parts:
        return "", False, False

    # FRM si hay más de 1 par (grupo,actividad)
    use_frm = len(unique_pairs) > 1

    bodyAgg = build_agg_with_signs(parts, signs)
    where_block = build_where_block(where_map)

    desc_sql = "'" + descripcion.replace("'", "''") + "'" if not (descripcion.startswith("'") and descripcion.endswith("'")) else descripcion

    sql1 = build_select_header(indice, desc_sql, use_frm)
    sql3 = build_from_where(where_block)
    sql4 = build_group_by(use_frm) + "\nUnion All"

    return (sql1 + "\n" + bodyAgg + "\n" + sql3 + "\n" + sql4), is_composite_expression(expr), use_frm

# -------------------- IO Excel y .sql --------------------

def process_workbook(input_path: str, sheet_name: str, first_row: int, last_row: int,
                     expr_col: int, sql_col: int, flag_col: int, frm_col: int, desc_col: int,
                     inplace: bool, output_path: Optional[str],
                     sql_out: Optional[str],
                     periodo_i: Optional[int], periodo_f: Optional[int]) -> None:
    wb: Workbook = load_workbook(filename=input_path)
    if sheet_name not in wb.sheetnames:
        raise ValueError(f"No existe la hoja '{sheet_name}' en {input_path}")
    ws = wb[sheet_name]

    sql_chunks: List[str] = []
    indice = 1
    for r in range(first_row, last_row + 1):
        expr = ws.cell(row=r, column=expr_col).value
        if expr is None or str(expr).strip() == "":
            ws.cell(row=r, column=sql_col).value = None
            ws.cell(row=r, column=flag_col).value = None
            if frm_col:
                ws.cell(row=r, column=frm_col).value = None
            continue

        desc = ws.cell(row=r, column=desc_col).value
        desc = "" if desc is None else str(desc)

        sql, is_comp, used_frm = build_sql_for_expression(expr, desc, indice)

        if sql:
            ws.cell(row=r, column=sql_col).value = sql
            ws.cell(row=r, column=flag_col).value = "compuesto" if is_comp else ""
            if frm_col:
                ws.cell(row=r, column=frm_col).value = "FRM" if used_frm else ""
            sql_chunks.append(sql)
            indice += 1
        else:
            ws.cell(row=r, column=sql_col).value = "-- (Sin resultado: expresión no reconocida)"
            ws.cell(row=r, column=flag_col).value = ""
            if frm_col:
                ws.cell(row=r, column=frm_col).value = ""

    # Guardar Excel
    if inplace:
        wb.save(input_path)
        excel_out_path = input_path
    else:
        if not output_path:
            output_path = input_path.rsplit(".", 1)[0] + "_out.xlsx"
        wb.save(output_path)
        excel_out_path = output_path

    # Generar .sql consolidado
    if sql_out:
        # concatenar y quitar el último 'Union'
        body = "\n".join(sql_chunks).rstrip()
        if body.endswith("Union All"):
            body = body[:-5].rstrip()
        header_lines = [
            "-- ===============================================================",
            "-- Archivo SQL autogenerado por generador_sql_metas_FRM.py",
            "-- ===============================================================",
        ]
        if periodo_i is not None and periodo_f is not None:
            header_lines.append(f"DECLARE @PERIODOI INT = {periodo_i};")
            header_lines.append(f"DECLARE @PERIODOf INT = {periodo_f};")
        header = "\n".join(header_lines) + "\n"
        with open(sql_out, "w", encoding="utf-8") as f:
            f.write(header + body + ";\n")

    print("OK")
    print(f"Excel actualizado: {excel_out_path}")
    if sql_out:
        print(f"SQL consolidado: {sql_out}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Ruta del Excel de entrada")
    ap.add_argument("--sheet", default="Generador de PLSQL (2)")
    ap.add_argument("--first-row", type=int, default=6)
    ap.add_argument("--last-row", type=int, default=314)
    ap.add_argument("--expr-col", type=int, default=10)  # J
    ap.add_argument("--sql-col", type=int, default=11)   # K
    ap.add_argument("--flag-col", type=int, default=12)  # L
    ap.add_argument("--frm-col", type=int, default=13)   # M (nuevo: marca FRM)
    ap.add_argument("--desc-col", type=int, default=2)   # B
    ap.add_argument("--inplace", action="store_true", default=False)
    ap.add_argument("--output", default=None)
    ap.add_argument("--sql-out", default=None, help="Ruta del .sql consolidado")
    ap.add_argument("--periodo-i", type=int, default=None)
    ap.add_argument("--periodo-f", type=int, default=None)

    args = ap.parse_args()
    process_workbook(
        input_path=args.input,
        sheet_name=args.sheet,
        first_row=args.first_row,
        last_row=args.last_row,
        expr_col=args.expr_col,
        sql_col=args.sql_col,
        flag_col=args.flag_col,
        frm_col=args.frm_col,
        desc_col=args.desc_col,
        inplace=args.inplace,
        output_path=args.output,
        sql_out=args.sql_out,
        periodo_i=args.periodo_i,
        periodo_f=args.periodo_f
    )

if __name__ == "__main__":
    main()
