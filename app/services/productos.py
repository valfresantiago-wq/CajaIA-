from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.deps import require_owner
from app.view import templates
from database.conexion import conectar
from servicios.servicio_stock import ajustar_stock

router = APIRouter(tags=["productos"])

@router.get("/productos", response_class=HTMLResponse)
def productos_page(request: Request, q: str = ""):
    user = require_owner(request)
    c = conectar()
    try:
        patron = f"%{q.strip()}%"
        rows = c.execute("""SELECT * FROM productos WHERE activo=1 AND (?='' OR nombre LIKE ? OR codigo_barras LIKE ?) ORDER BY nombre LIMIT 500""", (q.strip(), patron, patron)).fetchall()
    finally: c.close()
    return templates.TemplateResponse(request, "productos.html", {"user": user, "rows": rows, "q": q, "section": "productos"})

@router.post("/productos/{producto_id}/stock")
def stock_update(request: Request, producto_id: int, nuevo_stock: int = Form(...), motivo: str = Form(...)):
    user = require_owner(request)
    ajustar_stock(producto_id, nuevo_stock, user.id, motivo)
    return RedirectResponse("/productos", status_code=303)

@router.get("/stock", response_class=HTMLResponse)
def stock_page(request: Request):
    user = require_owner(request)
    c=conectar()
    try: rows=c.execute("SELECT * FROM productos WHERE activo=1 ORDER BY (stock<=stock_minimo) DESC, nombre LIMIT 1000").fetchall()
    finally:c.close()
    return templates.TemplateResponse(request, "stock.html", {"user":user,"rows":rows,"section":"stock"})
