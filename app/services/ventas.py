from decimal import Decimal
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.deps import require_user
from app.view import templates
from database.modelos import ItemVenta
from repositorios import productos
from servicios.servicio_promociones_grupo import aplicar as aplicar_promos
from servicios.servicio_ventas import registrar_venta
from seguridad.permisos import Permiso, exigir_permiso

router = APIRouter(prefix="/ventas", tags=["ventas"])

class ItemIn(BaseModel):
    producto_id: int
    cantidad: int = Field(ge=1)

class VentaIn(BaseModel):
    items: list[ItemIn]
    medio_pago: str
    efectivo_recibido: float | None = None
    referencia_pago: str | None = None
    cuotas: int | None = None

@router.get("", response_class=HTMLResponse)
def pantalla(request: Request):
    user = require_user(request)
    exigir_permiso(user, Permiso.FACTURAR)
    return templates.TemplateResponse(request, "ventas.html", {"user": user, "section": "ventas"})

@router.get("/api/productos")
def buscar_productos(request: Request, q: str = ""):
    user = require_user(request)
    exigir_permiso(user, Permiso.FACTURAR)
    rows = productos.listar(q.strip())[:30]
    return [{
        "id": p.id, "codigo": p.codigo_barras, "nombre": p.nombre,
        "precio": float(p.precio_venta), "stock": p.stock,
        "promo_cantidad": p.cantidad_promocional,
        "promo_precio": float(p.precio_promocional),
    } for p in rows]

@router.post("/api/confirmar")
def confirmar(request: Request, payload: VentaIn):
    user = require_user(request)
    exigir_permiso(user, Permiso.FACTURAR)
    items = []
    for req in payload.items:
        p = productos.obtener_por_id(req.producto_id)
        if not p:
            raise HTTPException(404, f"Producto {req.producto_id} no encontrado")
        items.append(ItemVenta(
            producto_id=p.id, codigo_barras=p.codigo_barras, nombre=p.nombre,
            cantidad=req.cantidad, precio_unitario=Decimal(str(p.precio_venta)),
            cantidad_promocional=p.cantidad_promocional,
            precio_promocional=Decimal(str(p.precio_promocional)),
        ))
    promos = aplicar_promos(items)
    venta_id, numero, total, vuelto = registrar_venta(
        usuario_id=user.id, items=items, medio_pago=payload.medio_pago,
        efectivo_recibido=Decimal(str(payload.efectivo_recibido)) if payload.efectivo_recibido is not None else None,
        referencia_pago=payload.referencia_pago, cuotas=payload.cuotas,
    )
    return {"ok": True, "venta_id": venta_id, "numero": numero, "total": float(total), "vuelto": float(vuelto), "promociones": promos}
