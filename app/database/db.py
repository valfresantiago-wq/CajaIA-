import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# =========================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./libreya_web.db"
)


# Render/PostgreSQL a veces entrega URLs antiguas con:
# postgres://
# SQLAlchemy necesita:
# postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )


# =========================================================
# MOTOR
# =========================================================

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)


# =========================================================
# SESIONES
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =========================================================
# BASE PARA LOS MODELOS
# =========================================================

Base = declarative_base()


# =========================================================
# DEPENDENCIA PARA FASTAPI
# =========================================================

def get_db():
    """
    Abre una sesión de base de datos para cada solicitud
    y la cierra automáticamente al terminar.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================================================
# CREACIÓN DE TABLAS
# =========================================================

def crear_tablas():
    """
    Crea las tablas registradas en Base.metadata.

    Debe ejecutarse después de importar los modelos.
    """

    Base.metadata.create_all(
        bind=engine
    )
