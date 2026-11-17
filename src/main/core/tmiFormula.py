"""Fórmula de un indicador del TMI escrita con términos de TOTALIZADO3:

    ([3;50] - [3;49]) / [3;47]
    [3;47] / MEDIANA([3;51])
    [5;19#77] / ([5;18] + [5;19#77] + [5;19#78]) * 100

Término  [grupo;actividad]             suma de cantidad de TOTALIZADO3 con ese grupo y actividad (todos los servicios)
         [grupo;actividad#servicios]   uno o varios servicios (#0, #77, #77,78)
         [grupo;actividad@CONDICION]   solo las filas cuya tipohoja tiene esa condición en DIM_HOJA para el año
                                       (los espacios de la condición van como _: NO ASEGURADO -> @NO_ASEGURADO)
                                       (#servicios@CONDICION si también filtra servicios), como Generar_pivot.sql:
                                       [1;1@ASEGURADO] = consultantes asegurados
Mediana (recursos), como CONSO1..CONSO14.sql: la mediana de cada servicio, redondeada, y suma de servicios.
Cada función dice cómo se toma el mes y el acumulado (enero..mes, tipo de cálculo ACUMULADO):
    MEDIANA([...])          mes: mediana        acumulado: mediana de todas las filas del periodo   (CONSO1..10, 12..14)
    MEDIANA_PERIODO([...])  mes: suma           acumulado: mediana de todas las filas del periodo   (CONSO11)
    [...]                   mes: suma           acumulado: suma de los meses
Como en CONSO, la mediana se saca por grupo, actividad y servicio: una variable con varios conjuntos suma la mediana
de cada conjunto (MEDIANA([3;51]) + MEDIANA([3;52#4])), nunca mezcla registros de distinto grupo o actividad.
Operadores + - * / , paréntesis y números.

El usuario no escribe estos términos: escribe la fórmula con letras (A, B, C...), cada una una
variable (tmi_variable), y aquí se expande a términos (expandir_alias):

    (A - B) / C   con A = Días Cama Disponible, B = Pacientes Días, C = Egresos   ->   ([3;50] - [3;49]) / [3;47]

La fórmula se analiza aquí y nunca se ejecuta como texto: cada término distinto recibe un código (T1, T2...) y la
expresión se traduce a SQL solo con esos códigos, números y operadores (formula_sql). Nada de esto se guarda: el
backend lo arma cada vez que calcula (tmiBaseRep.crear_tablas_formula -> #formula y #termino).

Regla de nulos (la elige el usuario por indicador: tmi_indicador.si_variable_nula / si_division_cero):
    si_variable_nula  CERO  término sin dato = 0             ISNULL(p.[T1],0)          (por defecto)
                      NA    término sin dato = NA ese mes    p.[T1]
    si_division_cero  NA    x / 0 = NA ese mes               x / NULLIF(y,0)           (por defecto)
                      CERO  x / 0 = 0                        ISNULL(x / NULLIF(y,0), 0)
CERO + CERO es la lógica de 00_TMI_CREACION_VISTAS_2025.sql: ISNULL(ISNULL(A,0) / NULLIF(ISNULL(B,0),0), 0).
Con NA + CERO solo la división entre 0 da 0: un término sin dato sigue dejando NA (0 * x * y es NULL si falta uno).
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


class ErrorFormula(ValueError):
    pass


REGLAS_NULO = ("CERO", "NA")

# función del término -> (mediana en el mes, mediana del periodo en el acumulado)
FUNCIONES = {"MEDIANA": (True, True), "MEDIANA_PERIODO": (False, True)}
# cálculo de la variable (agregacion, total_anual) -> función del término (None = término sin función: suma).
# Una variable MEDIANA siempre acumula con la mediana del periodo (no hay MEDIANA + suma de los meses).
_FUNCION_VARIABLE = {("MEDIANA", "MEDIANA_PERIODO"): "MEDIANA", ("SUMA", "MEDIANA_PERIODO"): "MEDIANA_PERIODO",
                     ("SUMA", "SUMA_MESES"): None}


@dataclass(frozen=True)
class Termino:
    tipgrupo: int
    actividad: int
    servicios: Tuple[int, ...]   # vacío = todos
    mediana: bool = False             # mes: mediana de cada servicio (si no, suma)
    condicion: Optional[str] = None   # DIM_HOJA.condicion de la tipohoja de TOTALIZADO3; None = todas las hojas
    periodo_mediana: bool = False     # acumulado: mediana de cada servicio en el periodo (si no, suma de los meses)

    @property
    def funcion(self) -> Optional[str]:
        return next((n for n, v in FUNCIONES.items() if v == (self.mediana, self.periodo_mediana)), None)

    @property
    def texto(self) -> str:
        serv = f"#{','.join(map(str, self.servicios))}" if self.servicios else ""
        cond = f"@{self.condicion}" if self.condicion else ""
        t = f"[{self.tipgrupo};{self.actividad}{serv}{cond}]"
        return f"{self.funcion}({t})" if self.funcion else t


@dataclass
class Formula:
    texto: str
    terminos: List[Termino] = field(default_factory=list)   # en orden de aparición: T1, T2...
    sql: str = ""
    si_variable_nula: str = "CERO"   # regla de nulos con la que se generó sql
    si_division_cero: str = "NA"

    def codigo(self, t: Termino) -> str:
        return f"T{self.terminos.index(t) + 1}"


_TOKEN = re.compile(r"""
    \s*(?:
      (?P<termino>\[\s*\d+\s*;\s*\d+\s*(?:\#\s*\d+(?:\s*,\s*\d+)*\s*)?(?:@\s*[A-Za-z0-9_]{1,20}\s*)?\])
    | (?P<mediana>MEDIANA(?:_PERIODO)?\b)
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
                               "Use términos [grupo;actividad], [grupo;actividad#servicio] o [grupo;actividad@CONDICION], "
                               "números, + - * / y paréntesis.")
        tipo = m.lastgroup
        salida.append((tipo, m.group(tipo), m.start(tipo) + 1))
        pos = m.end()
    return salida


def _termino(txt: str, funcion: Optional[str] = None) -> Termino:
    """funcion: MEDIANA o MEDIANA_PERIODO (None = término sin función)."""
    cuerpo = txt.strip()[1:-1].replace(" ", "")
    cuerpo, _, cond = cuerpo.partition("@")
    ga, _, serv = cuerpo.partition("#")
    g, a = (int(x) for x in ga.split(";"))
    servicios = tuple(sorted({int(s) for s in serv.split(",") if s})) if serv else ()
    mediana, periodo = FUNCIONES[funcion.upper()] if funcion else (False, False)
    return Termino(g, a, servicios, mediana, cond.upper() or None, periodo)



class _Parser:
    """expr := term (('+'|'-') term)* ; term := factor (('*'|'/') factor)* ;
    factor := número | término | MEDIANA(término) | (expr) | -factor"""

    def __init__(self, texto: str, si_variable_nula: str = "CERO", si_division_cero: str = "NA"):
        self.f = Formula(texto.strip())
        self.t = _tokens(texto)
        self.i = 0
        self.variable_cero = (si_variable_nula or "CERO").upper() == "CERO"
        self.division_cero = (si_division_cero or "NA").upper() == "CERO"

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
        col = f"p.[{self.f.codigo(t)}]"
        return f"ISNULL({col},0)" if self.variable_cero else col

    def dividir(self, s: str, d: str) -> str:
        """División según la regla del indicador. NA: x / 0 = NULL. CERO: x / 0 = 0; si además los términos pueden
        ser NULL (si_variable_nula = NA), un término sin dato sigue dando NULL: 0 * (x) * (y) es NULL si falta uno."""
        div = f"{s} / NULLIF({d},0)"
        if not self.division_cero:
            return div
        defecto = "0" if self.variable_cero else f"0 * ({s}) * ({d})"
        return f"ISNULL(({s}) / NULLIF({d},0), {defecto})"

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
            s = f"{s} * {d}" if op == "*" else self.dividir(s, d)
        return s

    def factor(self) -> str:
        tipo, v, pos = self.ver()
        if tipo == "numero":
            self.tomar()
            return v if "." in v else v + ".0"
        if tipo == "termino":
            self.tomar()
            return self.col(_termino(v))
        if tipo == "mediana":
            self.tomar()
            self.tomar("(")
            tipo2, v2, pos2 = self.tomar()
            if tipo2 != "termino":
                raise ErrorFormula(f"{v.upper()}( ) lleva un solo término [grupo;actividad] (posición {pos2}).")
            self.tomar(")")
            return self.col(_termino(v2, v))
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


def analizar(texto: Optional[str], si_variable_nula: str = "CERO", si_division_cero: str = "NA") -> Formula:
    """Valida la fórmula y devuelve sus términos (T1, T2...) y la expresión SQL sobre p.[T1], p.[T2]...
    con la regla de nulos del indicador (ver el inicio del módulo)."""
    if not texto or not texto.strip():
        raise ErrorFormula("Escriba la fórmula del indicador.")
    if len(texto) > 2000:
        raise ErrorFormula("La fórmula tiene más de 2000 caracteres.")
    for nombre, valor in (("si_variable_nula", si_variable_nula), ("si_division_cero", si_division_cero)):
        if (valor or "").upper() not in REGLAS_NULO:
            raise ErrorFormula(f"{nombre} debe ser CERO o NA.")
    p = _Parser(texto, si_variable_nula, si_division_cero)
    p.f.si_variable_nula, p.f.si_division_cero = si_variable_nula.upper(), si_division_cero.upper()
    p.f.sql = p.expr()
    if p.i < len(p.t):
        _, v, pos = p.ver()
        raise ErrorFormula(f"No se esperaba «{v}» en la posición {pos}.")
    if not p.f.terminos:
        raise ErrorFormula("La fórmula no tiene ningún término [grupo;actividad].")
    if len(p.f.terminos) > 60:
        raise ErrorFormula("La fórmula admite como máximo 60 términos distintos.")
    return p.f


def plantilla(f: Formula) -> str:
    """La fórmula con el código de cada término entre corchetes: ([T1] - [T2]) / [T3]. El cálculo reemplaza cada
    código por su valor para mostrar cómo se llegó al resultado (formula_desarrollo)."""
    salida, toks, i = [], _tokens(f.texto), 0
    while i < len(toks):
        tipo, v, _ = toks[i]
        if tipo == "mediana" and i + 3 < len(toks) and toks[i + 2][0] == "termino":
            salida.append(f"[{f.codigo(_termino(toks[i + 2][1], v))}]")
            i += 4
            continue
        salida.append(f"[{f.codigo(_termino(v))}]" if tipo == "termino" else v)
        i += 1
    return re.sub(r"\( | \)", lambda m: m.group(0).strip(), " ".join(salida))


def filas_termino(f: Formula):
    """Filas de #termino: una por término y servicio (servicio NULL = todos)."""
    for t in f.terminos:
        for s in (t.servicios or (None,)):
            yield {"codigo": f.codigo(t), "tipgrupo": t.tipgrupo, "actividad": t.actividad, "servicio": s,
                   "mediana": t.mediana, "periodo_mediana": t.periodo_mediana, "condicion": t.condicion,
                   "texto": t.texto}


_BASE_SEGURA = re.compile(r"^[A-Z0-9_]{1,30}$")


def consulta_sql(f: Formula, totalizado3: str, tipo_calculo: str, periodo: int, nombre: str = "",
                 centros: Optional[str] = None, indicador: Optional[dict] = None, esquema: Optional[str] = None,
                 dim: Optional[str] = None, cabecera: Optional[str] = None) -> str:
    """Query que calcula el indicador directo de TOTALIZADO3 para el periodo (AAAAMM): valor de cada término por
    centro y mes, acumulado de enero al mes si el cálculo es ACUMULADO, y la fórmula.
    centros: tabla/vista con codcentro, red y centro para los nombres (opcional).
    indicador ({"id", "base_estandar"}) y esquema (base.esquema de las tablas tmi_* y vistas vw_tmi_*): si vienen, agrega
    el estándar del mes de corte (mismo orden que usp_tmi_calcular) y las exclusiones del centro; los meses excluidos
    no suman en el ACUMULADO, como en el cálculo.
    dim (base.esquema de DIM_HOJA): hace falta si algún término tiene condición de hoja ([g;a@ASEGURADO]).
    cabecera: reemplaza el aviso y la regla de nulos del encabezado (la usa el SQL de una variable)."""
    filas = list(filas_termino(f))
    con_condicion = any(r["condicion"] for r in filas)
    if con_condicion and not dim:
        raise ErrorFormula("Falta la base de DIM_HOJA para la condición de hoja de los términos.")
    valores = ",\n        ".join(
        f"('{r['codigo']}', {r['tipgrupo']}, {r['actividad']}, "
        f"{'CAST(NULL AS INT)' if r['servicio'] is None else r['servicio']}, {1 if r['mediana'] else 0}, "
        f"{1 if r['periodo_mediana'] else 0}, "
        f"{'CAST(NULL AS VARCHAR(20))' if not r['condicion'] else repr(r['condicion'])})"
        for r in filas)
    # condición de hoja del término: solo las filas cuya tipohoja tiene esa condición en DIM_HOJA para el año
    filtro_hoja = (f"""
                     AND (k.condicion IS NULL OR T.tipohoja IN (
                          SELECT h.tipohoja FROM {dim}.DIM_HOJA h
                          WHERE CAST(h.ANIOHOJA AS INT) = @ANIO
                            AND REPLACE(UPPER(LTRIM(RTRIM(h.CONDICION))), ' ', '_') = k.condicion))"""
                   if con_condicion else "")
    grupos = ", ".join(str(g) for g in sorted({t.tipgrupo for t in f.terminos}))
    # ACUMULADO con mediana del periodo (MEDIANA / MEDIANA_PERIODO): la mediana de enero..mes (CTE periodo), como el
    # Total de CONSO1..CONSO14.sql; no la suma de los meses
    acum_periodo = tipo_calculo == "ACUMULADO" and any(t.periodo_mediana for t in f.terminos)

    def columna(t):
        c = f.codigo(t)
        if acum_periodo and t.periodo_mediana:
            return (f"(SELECT pr.valor FROM periodo pr WHERE pr.termino = '{c}' AND pr.codcentro = g.codcentro "
                    f"AND pr.mes = g.mes) AS [{c}]")
        return f"SUM(CASE WHEN v.termino = '{c}' THEN v.valor END) AS [{c}]"
    columnas = ",\n           ".join(columna(t) for t in f.terminos)
    leyenda = "\n".join(f"--   {f.codigo(t)} = {t.texto}" for t in f.terminos)
    union_mes = "v.mes <= g.mes" if tipo_calculo == "ACUMULADO" else "v.mes = g.mes"
    anio = int(periodo) // 100
    # meses como en el resultado final: los posteriores al corte salen 0
    meses = ",\n       ".join(f"CASE WHEN {m} > @MES THEN 0 ELSE MAX(CASE WHEN r.mes = {m} THEN r.valor END) END "
                               f"AS [{anio * 100 + m}]" for m in range(1, 13))
    centro_cte = f""",
centro AS (   -- centros de tmi_centro (como usp_tmi_calcular)
    SELECT c.codcentro, MIN(c.id_centro) AS id_centro, MAX(c.red) AS red, MAX(c.centro) AS centro,
           MAX(c.nivel) AS nivel, MAX(c.tipo) AS tipo, MAX(c.nivel_estandar) AS nivel_estandar, MAX(c.categoria) AS categoria
    FROM   {centros} c
    GROUP BY c.codcentro
)""" if centros else ""
    nombre_sql = "LEFT JOIN centro c ON c.codcentro = r.codcentro" if centros else ""
    if centros:
        # orden de tmi_centro (id); los centros que no están en tmi_centro van al final
        cols_centro = ("ROW_NUMBER() OVER (ORDER BY CASE WHEN MIN(c.id_centro) IS NULL THEN 1 ELSE 0 END, MIN(c.id_centro), "
                       "r.codcentro) AS ORDEN,\n"
                       "       MAX(c.red) AS Red, r.codcentro, MAX(c.centro) AS Centro, MAX(c.nivel) AS NIVEL, MAX(c.tipo) AS TIPO,")
    else:
        cols_centro = "ROW_NUMBER() OVER (ORDER BY r.codcentro) AS ORDEN, r.codcentro,"
    letra = "vale 0" if f.si_variable_nula == "CERO" else "deja NA (NULL)"
    division = "resultado 0" if f.si_division_cero == "CERO" else "deja NA (NULL)"
    aviso = """-- Calcula SOLO la fórmula sobre TOTALIZADO3. NO aplica estándares, puntajes, exclusiones, centros visibles
-- ni "centro sin datos en el año", y lista solo los centros con algún dato del indicador. El resultado
-- oficial del TMI es el de "Calcular" (usp_tmi_calcular)."""
    ctes_extra = declare_extra = excl_join = excl_periodo = cols_extra = filtro = ""
    salida_cte = """,
rs AS (SELECT codcentro, mes, valor, valor AS valor_total FROM r)"""
    universo = "SELECT DISTINCT codcentro FROM valores"
    # tablas que lee el query (para que el usuario sepa de dónde sale cada dato)
    tablas = [(totalizado3, "producción de cada término por centro y mes")]
    if con_condicion:
        tablas.append((f"{dim}.DIM_HOJA", "tipos de hoja de cada condición de hoja ([g;a@CONDICION])"))
    if centros:
        tablas.append((centros, "Red, Centro, NIVEL, TIPO y ORDEN (vista sobre tmi_centro)"))
    if indicador and esquema:
        tablas += [
            (f"{esquema}.fn_tmi_estandar", "estándar y % Acept del mes, la misma regla que Calcular. Lee "
                                           "vw_tmi_estandar_centro (tmi_estandar_centro), tmi_estandar, vw_tmi_std "
                                           "(tmi_estandar_tipo/nivel/categoria), tmi_indicador "
                                           "y tmi_indicador_acept"),
            (f"{esquema}.fn_tmi_exclusion", "meses excluidos y si quedan NA o 0, la misma regla que Calcular. Lee "
                                            "vw_tmi_exclusion (tmi_exclusion_centro_indicador)"),
        ]
    ancho = max(len(t) for t, _ in tablas)
    tablas_txt = "-- Tablas que usa este query:\n" + "\n".join(f"--   {t.ljust(ancho)}  {d}" for t, d in tablas)
    if indicador and esquema:
        id_ind = int(indicador["id"])
        base = str(indicador.get("base_estandar") or "").strip().upper()
        if base and not _BASE_SEGURA.match(base):   # vacío: solo estándar del centro y exclusiones
            raise ErrorFormula("El tipo de estándar del indicador no es válido.")
        e = esquema
        aviso = f"""-- Tabla como el resultado del TMI: Estandar del mes de corte (tipo de estándar {base or 'sin definir'}; el específico del
-- centro gana) y su % Acept (% Aceptmenos en banda), con las mismas funciones que Calcular (fn_tmi_estandar y
-- fn_tmi_exclusion: su definición se ve en SSMS). Exclusiones aplicadas a los meses:
-- mes excluido NA = vacío, mes excluido 0 = 0, y en ACUMULADO los meses excluidos no suman. Sin dato = 0.
-- Los centros sin estándar en el mes de corte no se muestran.
-- NO aplica puntajes, centros visibles por mes (flag), ámbito ni "centro sin datos en el año".
-- El resultado oficial del TMI es el de "Calcular"."""
        declare_extra = f"\nDECLARE @ID_INDICADOR INT = {id_ind};"
        if not centros:
            raise ErrorFormula("Falta la vista de centros para el estándar.")
        # regla única, la misma de usp_tmi_calcular (funciones de 04_procedimientos.sql)
        ctes_extra = f""",
excl AS (     -- meses excluidos: NA o 0 (la exclusión del indicador manda sobre la de "todos los indicadores")
    SELECT codcentro, mes, resultado, motivo
    FROM   {e}.fn_tmi_exclusion(@PERIODO)
    WHERE  id_indicador = @ID_INDICADOR
),
estandar AS (   -- estándar del mes de corte (el específico del centro gana) y su % Acept / % Aceptmenos
    SELECT codcentro, estandar, acept, aceptmenos, origen_estandar
    FROM   {e}.fn_tmi_estandar(@PERIODO)
    WHERE  id_indicador = @ID_INDICADOR
)"""
        universo = "SELECT codcentro FROM valores UNION SELECT codcentro FROM excl"
        if tipo_calculo == "ACUMULADO":
            excl_join = "\n                         AND NOT EXISTS (SELECT 1 FROM excl x WHERE x.codcentro = v.codcentro AND x.mes = v.mes)"
            excl_periodo = "\n                  AND NOT EXISTS (SELECT 1 FROM excl x WHERE x.codcentro = b.codcentro AND x.mes = b.mes)"
        nombre_sql += "\nLEFT JOIN estandar es ON es.codcentro = r.codcentro"
        # estándar del mes de corte (ya con el específico del centro) y su % Acept; % Aceptmenos solo si es banda
        cols_extra = ("\n       MAX(es.estandar) AS Estandar, MAX(es.acept) AS [% Acept],"
                      + (" MAX(es.aceptmenos) AS [% Aceptmenos]," if str(indicador.get("sentido") or "").upper() == "BANDA"
                         else ""))
        # mes excluido: NA = vacío, 0 = 0; el resto como el resultado final (sin dato = 0)
        filtro = "\nHAVING MAX(es.estandar) IS NOT NULL   -- centro sin estándar en el mes de corte: no se muestra"
        salida_cte = """,
rs AS (   -- exclusiones aplicadas al valor de cada mes
    SELECT r.codcentro, r.mes,
           CASE x.resultado WHEN 'NA' THEN NULL WHEN '0' THEN 0 ELSE ISNULL(r.valor, 0) END AS valor,
           -- Total como Calcular: si la fórmula da NA en el mes de corte (división entre 0 con la regla NA), el
           -- Total queda NA (SIN_DATO); las columnas de los meses lo muestran 0, como el resultado final
           CASE x.resultado WHEN 'NA' THEN NULL WHEN '0' THEN 0 ELSE r.valor END AS valor_total
    FROM   r
    LEFT JOIN excl x ON x.codcentro = r.codcentro AND x.mes = r.mes
)"""
    periodo_cte = f""",
periodo AS (   -- mediana del periodo: en cada mes, mediana de cada servicio con enero..mes, redondeada, y suma
    SELECT termino, codcentro, mes, SUM(ROUND(med, 0)) AS valor
    FROM  (SELECT termino, codcentro, mes, servicio, AVG(cantidad) AS med
           FROM  (SELECT b.termino, b.codcentro, k.mes, b.servicio, b.cantidad,
                         ROW_NUMBER() OVER (PARTITION BY b.termino, b.codcentro, k.mes, b.servicio ORDER BY b.cantidad) AS rn,
                         COUNT(*) OVER (PARTITION BY b.termino, b.codcentro, k.mes, b.servicio) AS cnt
                  FROM   base b
                  JOIN  (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) k (mes)
                         ON b.mes <= k.mes AND k.mes <= @MES
                  WHERE  b.periodo_mediana = 1{excl_periodo}) r
           WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
           GROUP BY termino, codcentro, mes, servicio) m
    GROUP BY termino, codcentro, mes
)""" if acum_periodo else ""
    if cabecera is None:
        cabecera = (f"-- Periodo: {int(periodo)}. Query para probar la fórmula en SQL Server (solo lectura: no modifica tablas).\n"
                    f"{aviso}\n-- Regla de nulos: letra sin datos {letra}; división entre 0 {division}.")
    return f"""-- {nombre}
{cabecera}
-- Fórmula: {f.texto}
{leyenda}
-- Cálculo: {tipo_calculo} ({'enero..mes' if tipo_calculo == 'ACUMULADO' else 'valor del mes'})
{tablas_txt}
DECLARE @PERIODO INT = {int(periodo)};   -- periodo AAAAMM: cámbielo aquí para probar otro mes
DECLARE @ANIO INT = @PERIODO / 100, @MES INT = @PERIODO % 100;{declare_extra}

WITH terminos (termino, tipgrupo, actividad, servicio, mediana, periodo_mediana, condicion) AS (
    SELECT * FROM (VALUES
        {valores}) x (termino, tipgrupo, actividad, servicio, mediana, periodo_mediana, condicion)
),
base AS (   -- registros de TOTALIZADO3 de cada término
    SELECT k.termino, k.mediana, k.periodo_mediana, T.codcentro_ses AS codcentro, T.periodo % 100 AS mes, T.servicio,
           CAST(T.cantidad AS FLOAT) AS cantidad
    FROM   {totalizado3} T
    JOIN   terminos k ON k.tipgrupo = T.tipgrupo AND k.actividad = T.actividad
                     AND (k.servicio IS NULL OR k.servicio = T.servicio){filtro_hoja}
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
){centro_cte}{ctes_extra}{periodo_cte},
grilla AS (
    SELECT c.codcentro, m.mes
    FROM  ({universo}) c
    CROSS JOIN (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) m (mes)
    WHERE  m.mes <= @MES
),
p AS (   -- términos como columnas
    SELECT g.codcentro, g.mes,
           {columnas}
    FROM   grilla g
    LEFT JOIN valores v ON v.codcentro = g.codcentro AND {union_mes}{excl_join}
    GROUP BY g.codcentro, g.mes
),
r AS (
    SELECT p.codcentro, p.mes, {f.sql} AS valor
    FROM   p
){salida_cte}
SELECT {cols_centro}{cols_extra}
       MAX(CASE WHEN r.mes = @MES THEN r.valor_total END) AS Total,
       {meses}
FROM   rs r
{nombre_sql}
GROUP BY r.codcentro{filtro}
ORDER BY ORDEN;"""


# ---------- Fórmula con letras ----------

# Conjuntos (tipgrupo, actividad, servicio) de una variable y de sus componentes activos (compuestas, hasta 10 niveles).
# {esq} = base.esquema de las tablas tmi_*, {p} = marcador del parámetro (:id en SQLAlchemy, ? en pyodbc; va dos veces).
def consulta_variable_sql(expresion: str, totalizado3: str, periodo: int, nombre: str, total_anual: str,
                          centros: Optional[str] = None, dim: Optional[str] = None) -> str:
    """Archivo .sql para probar una variable en SSMS: dos queries separados por GO sobre TOTALIZADO3.
    1) valor de cada mes (como la primera etapa del cálculo); 2) de enero a cada mes: su Total es el total anual de
    la variable (suma de los meses, o la mediana del periodo si la variable la usa)."""
    f = analizar(expresion)
    total = "la mediana del periodo" if (total_anual or "").upper() == "MEDIANA_PERIODO" else "la suma de los meses"
    comun = ("-- Calcula SOLO la variable sobre TOTALIZADO3 (solo lectura: no modifica tablas). No aplica exclusiones,\n"
             "-- estándares ni centros visibles, y lista solo los centros con algún dato de la variable.")
    partes = [
        (f"-- 1) Valor de cada mes. Total = valor del mes {int(periodo) % 100:02d}.\n{comun}", "MENSUAL"),
        (f"-- 2) De enero a cada mes. Total = total anual de la variable hasta el mes {int(periodo) % 100:02d} "
         f"({total}).\n{comun}", "ACUMULADO"),
    ]
    return "\nGO\n\n".join(
        consulta_sql(f, totalizado3, tipo, periodo, f"Variable: {nombre} · periodo {int(periodo)}", centros=centros,
                     dim=dim, cabecera=cab)
        for cab, tipo in partes) + "\nGO\n"


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
    SELECT l.tipgrupo, l.actividad, l.servicio, l.condicion_hoja
    FROM arbol a
    JOIN {esq}.tmi_variable_logica l ON l.id_variable = a.id_var AND l.activo = 1
    OPTION (MAXRECURSION 20)"""


def expresion_variable(nombre: str, agregacion: str, conjuntos,
                       total_anual: Optional[str] = None) -> Tuple[str, Optional[str]]:
    """Términos de una variable a partir de sus conjuntos (filas tipgrupo, actividad, servicio, condicion_hoja).
    Se agrupan por grupo, actividad y condición de hoja: servicio NULL en alguno = sin #
    (todos), si no #s1,s2; con condición de hoja, @CONDICION (solo esas hojas de DIM_HOJA). Varios grupos se suman
    entre paréntesis; con mediana, cada grupo y actividad lleva su propia mediana por servicio y luego se suman, como
    en CONSO (MEDIANA([g;a]) + MEDIANA([g2;a2])). El cálculo de la variable (agregacion del mes y total_anual del acumulado) da la función:
    SUMA + SUMA_MESES -> [g;a] ; MEDIANA -> MEDIANA([g;a]) (siempre mediana del periodo, como
    CONSO) ; SUMA + MEDIANA_PERIODO -> MEDIANA_PERIODO([g;a]).
    Los conjuntos de una variable son un OR: un conjunto sin condición de hoja ya cuenta todas las hojas, así que el
    mismo grupo y actividad con condición queda dentro de él (no se suma dos veces) si cubre sus servicios.
    Devuelve (expresión, aviso)."""
    agregacion = (agregacion or "SUMA").upper()
    total_anual = "MEDIANA_PERIODO" if agregacion == "MEDIANA" else (total_anual or "SUMA_MESES").upper()
    if (agregacion, total_anual) not in _FUNCION_VARIABLE:
        raise ErrorFormula(f"La variable «{nombre}» tiene un cálculo no válido: {agregacion} / {total_anual}")
    funcion = _FUNCION_VARIABLE[(agregacion, total_anual)]
    grupos: dict = {}
    avisos = []
    for c in conjuntos:
        g, a, s = int(c[0]), int(c[1]), c[2]
        # en el término los espacios van como _ (NO ASEGURADO -> @NO_ASEGURADO); el cálculo compara igual con DIM_HOJA
        cond = ("_".join(str(c[3]).upper().split()) or None) if c[3] is not None else None
        if cond and not re.fullmatch(r"[A-Z0-9_]{1,20}", cond):
            raise ErrorFormula(f"La variable «{nombre}» tiene una condición de hoja no válida: {c[3]}")
        grupos.setdefault((g, a, cond), set()).add(None if s is None else int(s))
    if not grupos:
        raise ErrorFormula(f"La variable «{nombre}» no tiene conjuntos (grupo y actividad).")
    cubre = lambda todos, servs: None in todos or (None not in servs and servs <= todos)
    for (g, a, cond) in [k for k in grupos if k[2]]:
        todas = grupos.get((g, a, None))
        if todas is None:
            continue
        servs = grupos[(g, a, cond)]
        if cubre(todas, servs):
            del grupos[(g, a, cond)]   # ya lo cuenta el conjunto sin condición de hoja
        elif None in servs or todas & servs:
            avisos.append(f"[{g};{a}] está con y sin condición de hoja en servicios que se cruzan: puede contarse dos veces.")
    terminos = []
    for (g, a, cond), servicios in sorted(grupos.items(), key=lambda x: (x[0][0], x[0][1], x[0][2] or "")):
        serv = "" if None in servicios else "#" + ",".join(str(x) for x in sorted(servicios))
        t = f"[{g};{a}{serv}{'@' + cond if cond else ''}]"
        terminos.append(f"{funcion}({t})" if funcion else t)
    expr = " + ".join(terminos)
    return (f"({expr})" if len(terminos) > 1 else expr), (" ".join(dict.fromkeys(avisos)) or None)


_TOKEN_ALIAS = re.compile(r"\s*(?:(?P<letra>[A-Z])|(?P<numero>\d+(?:\.\d+)?|\.\d+)|(?P<op>[-+*/()]))")


def letras_usadas(formula_alias: str) -> List[str]:
    return sorted(set(re.findall(r"[A-Z]", formula_alias or "")))


# formula_variable: la fórmula con letras con el id de la variable de cada letra entre llaves (A / B -> {1} / {2})
_ID_VARIABLE = re.compile(r"\{(\d+)\}")


def formula_con_ids(formula_alias: str, mapa: dict) -> str:
    """(A - B) * 100 con {"A": 1, "B": 2} -> ({1} - {2}) * 100. Cada letra de la fórmula debe tener variable."""
    faltan = [l for l in letras_usadas(formula_alias) if l not in mapa]
    if faltan:
        raise ErrorFormula("Falta la variable de la letra " + ", ".join(faltan) + ".")
    return re.sub(r"[A-Z]", lambda m: "{%d}" % int(mapa[m.group()]), formula_alias or "")


def letras_de_formula(formula_alias: Optional[str], formula_variable: Optional[str]) -> dict:
    """Variable de cada letra: la letra en formula_alias y el id en la misma posición de formula_variable.
    (A - B) * 100 y ({1} - {2}) * 100 -> {"A": 1, "B": 2}. Si no coinciden, ErrorFormula."""
    letras = re.findall(r"[A-Z]", formula_alias or "")
    ids = [int(x) for x in _ID_VARIABLE.findall(formula_variable or "")]
    mapa: dict = {}
    if len(letras) == len(ids):
        for letra, id_var in zip(letras, ids):
            if mapa.setdefault(letra, id_var) != id_var:
                break
        else:
            if formula_con_ids(formula_alias, mapa) == formula_variable:
                return mapa
    raise ErrorFormula("La fórmula con letras no coincide con la variable de cada letra (formula_variable).")


def ids_variables(formula_variable: Optional[str]) -> set:
    """Ids de las variables que usa la fórmula: {1} / {2} -> {1, 2}."""
    return {int(x) for x in _ID_VARIABLE.findall(formula_variable or "")}


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
