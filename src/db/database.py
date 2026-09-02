import os

from dotenv import load_dotenv
from src.core.config import require_env
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DB_CONFIG = {
    "host": require_env("DB_HOST"),
    "database": require_env("DB_NAME"),
    "user": require_env("DB_USER"),
    "password": require_env("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "1433"),
}

# sqlserver
query_params = {
    "driver": os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
}

if db_encrypt := (os.getenv("DB_ENCRYPT") or os.getenv("ENCRYPT")):
    query_params["encrypt"] = "yes" if db_encrypt.lower() in {"true", "yes", "1"} else "no"
if db_trust_cert := (os.getenv("DB_TRUST_SERVER_CERTIFICATE") or os.getenv("TRUSTSERVERCERTIFICATE")):
    query_params["trustServerCertificate"] = "yes" if db_trust_cert.lower() in {"true", "yes", "1"} else "no"

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="mssql+pyodbc",
    username=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database=DB_CONFIG["database"],
    query=query_params,
)

print("conexion a la base de datos: ", SQLALCHEMY_DATABASE_URL,query_params)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
    pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
 
