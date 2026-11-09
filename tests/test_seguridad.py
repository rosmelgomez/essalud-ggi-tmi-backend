"""Permisos (rol ADMIN + ACCESS_TMI) y mensajes de error sin datos internos. No consulta la base de datos: las
peticiones de prueba terminan antes (401/403 o validación del periodo)."""

import time

import jwt
import pytest
from fastapi.testclient import TestClient

from src.main.security import jwtTokenUtil as J
from src.main.security.errores import mensaje_seguro


@pytest.fixture(scope="module")
def cliente():
    import app as A
    return TestClient(A.app, raise_server_exceptions=False)   # sin "with": no corre el arranque (scripts SQL)


def cabecera(autoridades: str) -> dict:
    ahora = int(time.time())
    token = jwt.encode({"sub": "prueba", "authorities": autoridades, "token_type": "access",
                        "iat": ahora - 5, "exp": ahora + 600}, J.RAW_SECRET_KEY, algorithm=J.JWT_ALGORITHMS_PERMITIDOS[0])
    return {"Authorization": f"Bearer {token}"}


CALCULAR_FUTURO = "/tmi/dinamico/calcular/209912"   # si pasa el permiso responde 400 sin tocar la base


@pytest.mark.parametrize("autoridades, esperado", [
    ("USER", 403),
    ("ADMIN", 403),                       # falta access_tmi
    ("USER,ACCESS_TMI", 403),             # falta el rol
    ("ADMIN,ACCESS_TMI", 400),
    ("ROLE_ADMIN,ACCESS_TMI", 400),
])
def test_modificar_exige_admin_y_access_tmi(cliente, autoridades, esperado):
    assert cliente.post(CALCULAR_FUTURO, headers=cabecera(autoridades)).status_code == esperado


def test_sin_token_es_401(cliente):
    assert cliente.post(CALCULAR_FUTURO).status_code == 401


@pytest.mark.parametrize("ruta", ["/tmi/dinamico/ejecutar-sql", "/tmi/dinamico/indicadores/999999"])
def test_usuario_comun_no_ejecuta_scripts_ni_borra(cliente, ruta):
    metodo = cliente.post if ruta.endswith("ejecutar-sql") else cliente.delete
    assert metodo(ruta, headers=cabecera("USER")).status_code == 403


ODBC = "[42S02] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]"


def test_error_interno_no_muestra_nombres():
    msg = mensaje_seguro(f"(pyodbc.ProgrammingError) ('42S02', \"{ODBC}Invalid object name 'base.dbo.vw_x'. (208)\")", 500)
    assert "vw_x" not in msg and "código" in msg


def test_mensaje_propio_del_procedimiento_se_muestra():
    msg = mensaje_seguro(f"('42000', '{ODBC}TOTALIZADO3 no tiene datos del periodo 202612: no se calcula. (50000)')", 500)
    assert msg == "TOTALIZADO3 no tiene datos del periodo 202612: no se calcula."


def test_error_interno_relanzado_por_calcular_se_oculta():
    msg = mensaje_seguro(f"('42000', '{ODBC}[TMI-INTERNO] Error 208 en la línea 40 de usp_tmi_calcular: "
                         f"Invalid object name x. (50000)')", 500)
    assert "Invalid object" not in msg and "código" in msg


def test_clave_duplicada_tiene_mensaje_claro():
    assert mensaje_seguro(f"{ODBC}Violation of UNIQUE KEY constraint 'UX'. Cannot insert duplicate key", 400) \
        .startswith("Ya existe un registro con esos datos.")


def test_usuario_del_token_llega_al_endpoint_para_el_historial(cliente):
    """El middleware deja el usuario del token en USUARIO_ACTUAL; también en endpoints def (corren en otro hilo)."""
    import app as A
    from src.main.db.auditoria import USUARIO_ACTUAL
    if not any(getattr(r, "path", "") == "/prueba-usuario-historial" for r in A.app.routes):
        A.app.add_api_route("/prueba-usuario-historial", lambda: {"usuario": USUARIO_ACTUAL.get()}, methods=["GET"])
    c = cliente
    assert c.get("/prueba-usuario-historial", headers=cabecera("ADMIN,ACCESS_TMI")).json() == {"usuario": "prueba"}
    assert c.get("/prueba-usuario-historial").json() == {"usuario": None}
    assert USUARIO_ACTUAL.get() is None
