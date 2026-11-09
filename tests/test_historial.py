"""Historial de cambios: lectura de las filas XML de los triggers (sin base de datos)."""

from src.main.repositories import historialRep as H


def test_cambio_solo_muestra_campos_que_cambiaron():
    antes = H._fila('<fila id="7" estandar="4.000000000000000e+000" acept="5.0e+000" nivel="II"/>')
    despues = H._fila('<fila id="7" estandar="4.500000000000000e+000" acept="5.0e+000" nivel="II"/>')
    assert H._cambios("CAMBIO", antes, despues) == [{"campo": "estandar", "antes": 4, "despues": 4.5}]


def test_alta_y_baja_muestran_la_fila_y_null_no_aparece():
    fila = H._fila('<fila id="1" formula="[1;3] / [1;1]" activo="1"/>')
    assert H._cambios("ALTA", {}, fila) == [{"campo": "formula", "antes": None, "despues": "[1;3] / [1;1]"},
                                             {"campo": "activo", "antes": None, "despues": "1"}]
    assert [c["campo"] for c in H._cambios("BAJA", fila, {})] == ["formula", "activo"]
    assert H._fila(None) == {} and H._fila("<roto") == {}


def test_valores_numericos_y_texto():
    assert H._valor("1.000000000000000e-001") == 0.1
    assert H._valor("2026-01-01T00:00:00") == "2026-01-01T00:00:00"
    assert H._valor("TIPO_NIVEL") == "TIPO_NIVEL"

