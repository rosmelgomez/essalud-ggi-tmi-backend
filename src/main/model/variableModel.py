"""Variables: cómo se construye cada variable desde TOTALIZADO3."""

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.mssql import BIT, DATETIME

from src.main.model.base import AHORA, TMI_SCHEMA, Base, defecto


class TmiVariable(Base):
    __tablename__ = "tmi_variable"
    __table_args__ = (
        # la mediana del periodo solo tiene sentido en una variable MEDIANA
        CheckConstraint("agregacion IN ('SUMA', 'MEDIANA') AND total_anual IN ('SUMA_MESES', 'MEDIANA_PERIODO') "
                        "AND (agregacion = 'MEDIANA' OR total_anual = 'SUMA_MESES')", name="CK_tmi_variable_calculo"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False, unique=True)
    descripcion = Column(String(200))
    agregacion = Column(String(10), nullable=False, server_default=defecto("SUMA"))            # SUMA | MEDIANA
    total_anual = Column(String(15), nullable=False, server_default=defecto("SUMA_MESES"))     # SUMA_MESES | MEDIANA_PERIODO
    activo = Column(BIT, nullable=False, server_default=defecto(1))
    usuario_creacion = Column(String(200))
    fecha_creacion = Column(DATETIME, nullable=False, server_default=AHORA)
    usuario_modificacion = Column(String(200))
    fecha_modificacion = Column(DATETIME)


class TmiVariableLogica(Base):
    __tablename__ = "tmi_variable_logica"
    __table_args__ = {"schema": TMI_SCHEMA}
    id = Column(Integer, primary_key=True)
    id_variable = Column(Integer, ForeignKey(TmiVariable.id), nullable=False)
    tipgrupo = Column(Integer, nullable=False)                 # DIM_GRUPO.tipgrupo
    actividad = Column(Integer, nullable=False)                # DIM_ACTIVIDAD.actividad
    servicio = Column(Integer)                                 # TOTALIZADO3.servicio ; NULL = todos
    condicion_hoja = Column(String(20))                        # DIM_HOJA.condicion ; NULL = todas
    periodo_desde = Column(Integer, nullable=False, server_default=defecto(200001))
    periodo_hasta = Column(Integer, nullable=False, server_default=defecto(999912))
    activo = Column(BIT, nullable=False, server_default=defecto(1))


class TmiVariableComponente(Base):
    """Variables compuestas: la variable suma, además de su lógica, el valor de otras variables (componentes)."""
    __tablename__ = "tmi_variable_componente"
    __table_args__ = (
        UniqueConstraint("id_variable", "id_variable_componente", name="UX_tmi_variable_componente"),
        CheckConstraint("id_variable <> id_variable_componente", name="CK_tmi_variable_componente"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)
    id_variable = Column(Integer, ForeignKey(TmiVariable.id, name="FK_tmi_var_comp_variable"), nullable=False)
    id_variable_componente = Column(Integer, ForeignKey(TmiVariable.id, name="FK_tmi_var_comp_componente"),
                                    nullable=False)
    activo = Column(BIT, nullable=False, server_default=defecto(1))
