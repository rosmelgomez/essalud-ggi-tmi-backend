"""Fórmula de un indicador del TMI escrita con términos de TOTALIZADO3:

    ([3;50] - [3;49]) / [3;47]
    [3;47] / MEDIANA([3;51])
    [5;19#77] / ([5;18] + [5;19#77] + [5;19#78]) * 100

Término  [grupo;actividad]             suma de cantidad de TOTALIZADO3 con ese grupo y actividad (todos los servicios)
         [grupo;actividad#servicios]   uno o varios servicios (#0, #77, #77,78)
MEDIANA([...])                         mediana de cada servicio en el mes, redondeada, y suma de servicios (recursos)
Operadores + - * / , paréntesis y números.

El usuario no escribe estos términos: escribe la fórmula con letras (A, B, C...), cada una una
variable (tmi_variable), y aquí se expande a términos (expandir_alias):

    (A - B) / C   con A = Días Cama Disponible, B = Pacientes Días, C = Egresos   ->   ([3;50] - [3;49]) / [3;47]

La fórmula se analiza aquí y nunca se ejecuta como texto: cada término distinto recibe un código (T1, T2...) y la
expresión se traduce a SQL solo con esos códigos, números y operadores (formula_sql). Una división entre 0 da NULL.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


class ErrorFormula(ValueError):
    pass


@dataclass(frozen=True)
class Termino:
    tipgrupo: int
    actividad: int
    servicios: Tuple[int, ...]   # vacío = todos
    mediana: bool = False

    @property
    def texto(self) -> str:
        serv = f"#{','.join(map(str, self.servicios))}" if self.servicios else ""
        t = f"[{self.tipgrupo};{self.actividad}{serv}]"
        return f"MEDIANA({t})" if self.mediana else t


@dataclass
class Formula:
    texto: str
    terminos: List[Termino] = field(default_factory=list)   # en orden de aparición: T1, T2...
    sql: str = ""

    def codigo(self, t: Termino) -> str:
        return f"T{self.terminos.index(t) + 1}"


_TOKEN = re.compile(r"""
    \s*(?:
      (?P<termino>\[\s*\d+\s*;\s*\d+\s*(?:\#\s*\d+(?:\s*,\s*\d+)*\s*)?\])
    | (?P<mediana>MEDIANA\b)
    | (?P<numero>\d+(?:\.\d+)?)
    | (?P<op>[-+*/()])
    )""", re.VERBOSE | re.IGNORECASE)


def _tokens(texto: str):
    pos, salida = 0, []
    texto = texto.rstrip()
    while pos < len(texto):
        m = _TOKEN.match(texto, pos)
        if not m or m.end() == pos:
            resto = texto[pos:].strip()
            raise ErrorFormula(f"No se reconoce «{resto[:20]}» en la posición {pos + 1}. "
                               "Use términos [grupo;actividad] o [grupo;actividad#servicio], números, + - * / y paréntesis.")
        tipo = m.lastgroup
        salida.append((tipo, m.group(tipo), m.start(tipo) + 1))
        pos = m.end()
    return salida


def _termino(txt: str, mediana: bool) -> Termino:
    cuerpo = txt.strip()[1:-1].replace(" ", "")
    ga, _, serv = cuerpo.partition("#")
    g, a = (int(x) for x in ga.split(";"))
    servicios = tuple(sorted({int(s) for s in serv.split(",") if s})) if serv else ()
    return Termino(g, a, servicios, mediana)


class _Parser:
    """expr := term (('+'|'-') term)* ; term := factor (('*'|'/') factor)* ;
    factor := número | término | MEDIANA(término) | (expr) | -factor"""

    def __init__(self, texto: str):
        self.f = Formula(texto.strip())
        self.t = _tokens(texto)
        self.i = 0

    def ver(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None, len(self.f.texto) + 1)

    def tomar(self, valor=None):
        tipo, v, pos = self.ver()
        if tipo is None or (valor is not None and v != valor):
            raise ErrorFormula(f"Se esperaba «{valor}» en la posición {pos}." if valor else "La fórmula está incompleta.")
        self.i += 1
        return tipo, v, pos

    def col(self, t: Termino) -> str:
        if t not in self.f.terminos:
            self.f.terminos.append(t)
        return f"ISNULL(p.[{self.f.codigo(t)}],0)"

    def expr(self) -> str:
        s = self.term()
        while self.ver()[1] in ("+", "-"):
            op = self.tomar()[1]
            s = f"{s} {op} {self.term()}"
        return s

    def term(self) -> str:
        s = self.factor()
        while self.ver()[1] in ("*", "/"):
            op = self.tomar()[1]
            d = self.factor()
            s = f"{s} * {d}" if op == "*" else f"{s} / NULLIF({d},0)"
        return s

    def factor(self) -> str:
        tipo, v, pos = self.ver()
        if tipo == "numero":
            self.tomar()
            return v if "." in v else v + ".0"
        if tipo == "termino":
            self.tomar()
            return self.col(_termino(v, False))
        if tipo == "mediana":
            self.tomar()
            self.tomar("(")
            tipo2, v2, pos2 = self.tomar()
            if tipo2 != "termino":
                raise ErrorFormula(f"MEDIANA( ) lleva un solo término [grupo;actividad] (posición {pos2}).")
            self.tomar(")")
            return self.col(_termino(v2, True))
        if v == "(":
            self.tomar()
            s = self.expr()
            self.tomar(")")
            return f"({s})"
        if v == "-":
            self.tomar()
            return f"(-{self.factor()})"
        raise ErrorFormula(f"Falta un término o un número en la posición {pos}." if tipo is None or v in "+*/)"
                           else f"No se esperaba «{v}» en la posición {pos}.")


def analizar(texto: Optional[str]) -> Formula:
    """Valida la fórmula y devuelve sus términos (T1, T2...) y la expresión SQL sobre p.[T1], p.[T2]..."""
    if not texto or not texto.strip():
        raise ErrorFormula("Escriba la fórmula del indicador.")
    if len(texto) > 2000:
        raise ErrorFormula("La fórmula tiene más de 2000 caracteres.")
    p = _Parser(texto)
    p.f.sql = p.expr()
    if p.i < len(p.t):
        _, v, pos = p.ver()
        raise ErrorFormula(f"No se esperaba «{v}» en la posición {pos}.")
    if not p.f.terminos:
        raise ErrorFormula("La fórmula no tiene ningún término [grupo;actividad].")
    if len(p.f.terminos) > 60:
        raise ErrorFormula("La fórmula admite como máximo 60 términos distintos.")
    return p.f


def filas_termino(f: Formula):
    """Filas de tmi_indicador_termino: una por término y servicio (servicio NULL = todos)."""
    for t in f.terminos:
        for s in (t.servicios or (None,)):
            yield {"codigo": f.codigo(t), "tipgrupo": t.tipgrupo, "actividad": t.actividad, "servicio": s,
                   "mediana": t.mediana, "texto": t.texto}


def consulta_sql(f: Formula, totalizado3: str, tipo_calculo: str, periodo: int, nombre: str = "",
                 centros: Optional[str] = None) -> str:
    """Query que calcula el indicador directo de TOTALIZADO3 para el periodo (AAAAMM): valor de cada término por
    centro y mes, acumulado de enero al mes si el cálculo es ACUMULADO, y la fórmula. Sin estándares ni exclusiones
    (esos se aplican al Calcular). centros: tabla/vista con codcentro y centro para el nombre (opcional)."""
    filas = list(filas_termino(f))
    valores = ",\n        ".join(
        f"('{r['codigo']}', {r['tipgrupo']}, {r['actividad']}, "
        f"{'CAST(NULL AS INT)' if r['servicio'] is None else r['servicio']}, {1 if r['mediana'] else 0})"
        for r in filas)
    grupos = ", ".join(str(g) for g in sorted({t.tipgrupo for t in f.terminos}))
    columnas = ",\n           ".join(f"SUM(CASE WHEN v.termino = '{f.codigo(t)}' THEN v.valor END) AS [{f.codigo(t)}]"
                                     for t in f.terminos)
    leyenda = "\n".join(f"--   {f.codigo(t)} = {t.texto}" for t in f.terminos)
    union_mes = "v.mes <= g.mes" if tipo_calculo == "ACUMULADO" else "v.mes = g.mes"
    meses = ",\n       ".join(f"MAX(CASE WHEN r.mes = {m} THEN r.valor END) AS [{m:02d}]" for m in range(1, 13))
    nombre_sql = (f"LEFT JOIN (SELECT codcentro, MAX(centro) AS centro FROM {centros} GROUP BY codcentro) c "
                  "ON c.codcentro = r.codcentro") if centros else ""
    centro_col = "MAX(c.centro)" if centros else "CAST(NULL AS VARCHAR(200))"
    return f"""-- {nombre}
-- Fórmula: {f.texto}
{leyenda}
-- Cálculo: {tipo_calculo} ({'enero..mes' if tipo_calculo == 'ACUMULADO' else 'valor del mes'})
DECLARE @PERIODO INT = {int(periodo)};
DECLARE @ANIO INT = @PERIODO / 100, @MES INT = @PERIODO % 100;

WITH terminos (termino, tipgrupo, actividad, servicio, mediana) AS (
    SELECT * FROM (VALUES
        {valores}) x (termino, tipgrupo, actividad, servicio, mediana)
),
base AS (   -- registros de TOTALIZADO3 de cada término
    SELECT k.termino, k.mediana, T.codcentro_ses AS codcentro, T.periodo % 100 AS mes, T.servicio,
           CAST(T.cantidad AS FLOAT) AS cantidad
    FROM   {totalizado3} T
    JOIN   terminos k ON k.tipgrupo = T.tipgrupo AND k.actividad = T.actividad
                     AND (k.servicio IS NULL OR k.servicio = T.servicio)
    WHERE  T.periodo BETWEEN @ANIO * 100 + 1 AND @PERIODO AND T.tipgrupo IN ({grupos})
),
valores AS (   -- valor de cada término por centro y mes
    SELECT termino, codcentro, mes, SUM(cantidad) AS valor
    FROM   base WHERE mediana = 0
    GROUP BY termino, codcentro, mes
    UNION ALL
    SELECT termino, codcentro, mes, SUM(ROUND(med, 0))
    FROM  (SELECT termino, codcentro, mes, servicio, AVG(cantidad) AS med
           FROM  (SELECT termino, codcentro, mes, servicio, cantidad,
                         ROW_NUMBER() OVER (PARTITION BY termino, codcentro, mes, servicio ORDER BY cantidad) AS rn,
                         COUNT(*) OVER (PARTITION BY termino, codcentro, mes, servicio) AS cnt
                  FROM base WHERE mediana = 1) r
           WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
           GROUP BY termino, codcentro, mes, servicio) m
    GROUP BY termino, codcentro, mes
),
grilla AS (
    SELECT c.codcentro, m.mes
    FROM  (SELECT DISTINCT codcentro FROM valores) c
    CROSS JOIN (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) m (mes)
    WHERE  m.mes <= @MES
),
p AS (   -- términos como columnas
    SELECT g.codcentro, g.mes,
           {columnas}
    FROM   grilla g
    LEFT JOIN valores v ON v.codcentro = g.codcentro AND {union_mes}
    GROUP BY g.codcentro, g.mes
),
r AS (
    SELECT p.codcentro, p.mes, {f.sql} AS valor
    FROM   p
)
SELECT r.codcentro, {centro_col} AS centro,
       MAX(CASE WHEN r.mes = @MES THEN r.valor END) AS total,
       {meses}
FROM   r
{nombre_sql}
GROUP BY r.codcentro
ORDER BY r.codcentro;"""


# ---------- Fórmula con letras ----------

# Conjuntos (tipgrupo, actividad, servicio) de una variable y de sus componentes activos (compuestas, hasta 10 niveles).
# {esq} = base.esquema de las tablas tmi_*, {p} = marcador del parámetro (:id en SQLAlchemy, ? en pyodbc; va dos veces).
SQL_CONJUNTOS = """
    WITH arbol AS (
        SELECT CAST({p} AS INT) AS id_var, 0 AS nivel, CAST('/' + CAST({p} AS VARCHAR(10)) + '/' AS VARCHAR(400)) AS camino
        UNION ALL
        SELECT c.id_variable_componente, a.nivel + 1,
               CAST(a.camino + CAST(c.id_variable_componente AS VARCHAR(10)) + '/' AS VARCHAR(400))
        FROM arbol a
        JOIN {esq}.tmi_variable_componente c ON c.id_variable = a.id_var AND c.activo = 1
        WHERE a.nivel < 10 AND a.camino NOT LIKE '%/' + CAST(c.id_variable_componente AS VARCHAR(10)) + '/%'
    )
    SELECT l.tipgrupo, l.actividad, l.servicio, l.condicion_hoja, l.periodo_desde, l.periodo_hasta
    FROM arbol a
    JOIN {esq}.tmi_variable_logica l ON l.id_variable = a.id_var AND l.activo = 1
    OPTION (MAXRECURSION 20)"""


def expresion_variable(nombre: str, agregacion: str, conjuntos) -> Tuple[str, Optional[str]]:
    """Términos de una variable a partir de sus conjuntos (filas tipgrupo, actividad, servicio, condicion_hoja,
    periodo_desde, periodo_hasta). Se agrupan por grupo y actividad: servicio NULL en alguno = sin # (todos), si no #s1,s2.
    SUMA -> [g;a] o [g;a#s] ; MEDIANA -> MEDIANA([g;a]). Varios grupos se suman entre paréntesis.
    Devuelve (expresión, aviso): la condición de hoja y la vigencia de los conjuntos no se aplican en la fórmula."""
    grupos: dict = {}
    aviso = None
    for c in conjuntos:
        g, a, s = int(c[0]), int(c[1]), c[2]
        grupos.setdefault((g, a), set()).add(None if s is None else int(s))
        if c[3] or (c[4] and c[4] > 200001) or (c[5] and c[5] < 999912):
            aviso = "Tiene conjuntos con condición de hoja o vigencia: en la fórmula se toman siempre."
    if not grupos:
        raise ErrorFormula(f"La variable «{nombre}» no tiene conjuntos (grupo y actividad).")
    terminos = []
    for (g, a), servicios in sorted(grupos.items()):
        serv = "" if None in servicios else "#" + ",".join(str(x) for x in sorted(servicios))
        t = f"[{g};{a}{serv}]"
        terminos.append(f"MEDIANA({t})" if agregacion == "MEDIANA" else t)
    expr = " + ".join(terminos)
    return (f"({expr})" if len(terminos) > 1 else expr), aviso


_TOKEN_ALIAS = re.compile(r"\s*(?:(?P<letra>[A-Z])|(?P<numero>\d+(?:\.\d+)?|\.\d+)|(?P<op>[-+*/()]))")


def letras_usadas(formula_alias: str) -> List[str]:
    return sorted(set(re.findall(r"[A-Z]", formula_alias or "")))


def expandir_alias(formula_alias: Optional[str], mapa: dict) -> str:
    """Valida la fórmula con letras ((A - B) / C) y la devuelve con los términos de cada letra (mapa letra -> expresión).
    Los errores dan la posición en la fórmula con letras."""
    texto = (formula_alias or "").rstrip()
    if not texto.strip():
        raise ErrorFormula("Escriba la fórmula con las letras de las variables.")
    if len(texto) > 500:
        raise ErrorFormula("La fórmula tiene más de 500 caracteres.")
    tokens, pos = [], 0
    while pos < len(texto):
        m = _TOKEN_ALIAS.match(texto, pos)
        if not m:
            raise ErrorFormula(f"No se reconoce «{texto[pos:].strip()[:10]}» en la posición {pos + 1}.")
        tokens.append((m.lastgroup, m.group(m.lastgroup), m.start(m.lastgroup) + 1))
        pos = m.end()
    i = 0

    def ver():
        return tokens[i] if i < len(tokens) else (None, None, len(texto) + 1)

    def tomar():
        nonlocal i
        i += 1
        return tokens[i - 1]

    def expr() -> str:
        s = term()
        while ver()[1] in ("+", "-"):
            s += f" {tomar()[1]} {term()}"
        return s

    def term() -> str:
        s = factor()
        while ver()[1] in ("*", "/"):
            s += f" {tomar()[1]} {factor()}"
        return s

    def factor() -> str:
        tipo, v, p = ver()
        if tipo == "letra":
            tomar()
            if v not in mapa:
                raise ErrorFormula(f"La letra {v} no tiene variable: agréguela o quítela de la fórmula.")
            return mapa[v]
        if tipo == "numero":
            tomar()
            return v
        if v == "(":
            tomar()
            s = expr()
            if ver()[1] != ")":
                raise ErrorFormula(f"Falta cerrar el paréntesis «)» en la posición {ver()[2]}.")
            tomar()
            return f"({s})"
        if v == "-":
            tomar()
            return f"-{factor()}"
        if tipo is None:
            raise ErrorFormula("La fórmula está incompleta: falta una variable o un número al final.")
        raise ErrorFormula(f"Falta una variable o un número en la posición {p}.")

    resultado = expr()
    if i < len(tokens):
        tipo, v, p = ver()
        raise ErrorFormula(f"Falta una operación (+ − × ÷) antes de «{v}» en la posición {p}."
                           if tipo in ("letra", "numero") or v == "(" else f"No se esperaba «{v}» en la posición {p}.")
    return resultado
