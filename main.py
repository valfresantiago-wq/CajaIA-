from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import APP_NAME, APP_VERSION, COOKIE_SECURE, SECRET_KEY
from database.migraciones import ejecutar_migraciones
from database.auxiliar import conectar_aux
from app.routers import auth, dashboard, ventas, productos, rentabilidad, compras, catalogo, administracion

ROOT = Path(__file__).resolve().parents[1]


@asynccontextmanager
async def lifespan(app: FastAPI):
    ejecutar_migraciones()
    c = conectar_aux(); c.close()
    yield


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    https_only=COOKIE_SECURE,
    same_site="lax",
    max_age=60 * 60 * 12,
)
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(ventas.router)
app.include_router(productos.router)
app.include_router(rentabilidad.router)
app.include_router(compras.router)
app.include_router(catalogo.router)
app.include_router(administracion.router)


@app.get("/health")
def health():
    return {"ok": True, "app": APP_NAME, "version": APP_VERSION}
