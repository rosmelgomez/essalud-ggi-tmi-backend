"""Historial de cambios de la configuración del TMI (lo llenan los triggers de 06_historial.sql)."""

from sqlalchemy import Column, Index, Integer, String, UnicodeText
from sqlalchemy.dialects.mssql import DATETIME

from src.main.model.base import AHORA, TMI_SCHEMA, Base


class TmiConfigHistorial(Base):
    """Una fila por registro que cambió: quién, cuándo, en qué tabla, y la fila antes y después (XML de FOR XML RAW,
    sin las columnas de auditoría). usuario = el del token (CONTEXT_INFO que pone el backend); si el cambio no vino de
    la API (SSMS, scripts), el login de SQL Server."""
    __tablename__ = "tmi_config_historial"
    __table_args__ = (Index("IX_tmi_config_historial_indicador", "id_indicador", "fecha"),
                      Index("IX_tmi_config_historial_fecha", "fecha"),
                      {"schema": TMI_SCHEMA})
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DATETIME, nullable=False, server_default=AHORA)
    usuario = Column(String(128))
    tabla = Column(String(60), nullable=False)
    id_registro = Column(Integer)
    id_indicador = Column(Integer)
    accion = Column(String(10), nullable=False)                # ALTA | CAMBIO | BAJA
    antes = Column(UnicodeText)
    despues = Column(UnicodeText)
