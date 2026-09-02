from sqlalchemy.orm import decl_base
from sqlalchemy.orm import decl_base
from sqlalchemy.orm import decl_base
from src.dtos.dto import Estandar
from src.db.database import SessionLocal
from fastapi import HTTPException
from sqlalchemy import text


def queryEstandares(db: SessionLocal):
    try:
        query = f"""
        SElECT est.*
        FROM [pentahodev_prueba].[dbo].[estandares] est
        """
        result = db.execute(text(query))
        return result.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryEstandaresByCentro(db: SessionLocal, codcentro:str):
    try:
        query = f"""
          SElECT est.*, cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.nivel_estandar
          FROM [pentahodev_prueba].[dbo].[estandares] est
          JOIN [pentahodev_prueba].[dbo].[centros_tmi] cen ON est.nivel_estandar_centro = cen.nivel_estandar
          WHERE cen.codcentro = :codcentro
        """
        result = db.execute(text(query), {"codcentro": codcentro})
        return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandares(db: SessionLocal, dto:Estandar):
    try:
        query = f"""
        USE [pentahodev_prueba]
        GO

        UPDATE [dbo].[estandares]
          SET [id] = :id
          ,[orden_indicador] = :orden_indicador
          ,[codigo_unico] = :codigo_unico
          ,[tipo] = :tipo
          ,[indicador] = :indicador
          ,[nivel_centro] = :nivel_centro
          ,[tipo_centro] = :tipo_centro
          ,[nivel_estandar_centro] = :nivel_estandar_centro
          ,[estandar] = :estandar
          ,[acept] = :acept
          ,[aceptmenos] = :aceptmenos
        WHERE id = :id
        """

        result = db.execute(text(query), {"dto": dto})
        db.commit()
        return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def queryUpdateEstandaresCentros(db: SessionLocal, dto:Estandar):
    try:
        query = f"""
        USE [pentahodev_prueba]
        GO

        UPDATE [dbo].[centros_tmi]
            SET [id] = :id
            ,[red] = :red
            ,[orden] = :orden
            ,[orden_tipo] = :orden_tipo
            ,[codcentro] = :codcentro
            ,[tipo] = :tipo
            ,[nivel] = :nivel
            ,[nivel_estandar] = :nivel_estandar
            ,[centro] = :centro
            ,[estado] = :estado
        WHERE id = :id
        """
        result = db.execute(text(query), {"dto": dto})
        db.commit()
        return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))








