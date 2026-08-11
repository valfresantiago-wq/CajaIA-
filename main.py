from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import (
    APP_NAME,
    APP_VERSION,
    COOKIE_SECURE,
    SECRET_KEY,
)

from database.migraciones import ejecutar_migraciones
from database.auxiliar import conectar_aux

# Routers existentes
from app.routers import (
    auth,
    dashboard,
    ventas,
    productos,
    rentabilidad,
    compras,
    catalogo,
    administracion,
)

# Base SQLAlchemy web
from app.database.db import Base, engine

# Importamos modelos para que SQLAlchemy
# conozca todas las tablas antes de create_all()
from app.models.producto import Producto
from app.models.venta import Venta, DetalleVenta
from app.models.compra import Compra, DetalleCompra
from app.models.proveedor import Proveedor
from app.models.historial_costo import HistorialCosto


# =========================================================
# RUTAS DEL PROYECTO
# =========================================================

ROOT = Path(__file__).resolve().parent

STATIC_DIR = ROOT / "app" / "static"


# =========================================================
# INICIO / CIERRE DE LA APLICACIÓN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Migraciones del sistema heredado
    ejecutar_migraciones()

    # Base auxiliar existente
    conexion_aux = conectar_aux()
    conexion_aux.close()

    # Tablas SQLAlchemy web
    Base.metadata.create_all(
        bind=engine
    )

    yield


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan,
)


# =========================================================
# SESIONES
# =========================================================

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    https_only=COOKIE_SECURE,
    same_site="lax",
    max_age=60 * 60 * 12,
)


# =========================================================
# ARCHIVOS ESTÁTICOS
# =========================================================

app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static",
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(
    auth.router
)

app.include_router(
    dashboard.router
)

app.include_router(
    ventas.router
)

app.include_router(
    productos.router
)

app.include_router(
    rentabilidad.router
)

app.include_router(
    compras.router
)

app.include_router(
    indicadores.router
)

app.include_router(
    catalogo.router
)

app.include_router(
    administracion.router
)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "ok": True,
        "app": APP_NAME,
        "version": APP_VERSION,
    }
