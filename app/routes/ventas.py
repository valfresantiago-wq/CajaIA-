from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.producto import Producto
from app.models.venta import Venta, DetalleVenta


router = APIRouter(
    prefix="/api/ventas",
    tags=["Ventas"]
)


@router.post("")
def registrar_venta(
    datos: dict,
    db: Session = Depends(get_db)
):
    items = datos.get("items", [])

    if not items:
        raise HTTPException(
            status_code=400,
            detail="La venta no contiene productos"
        )

    venta = Venta(
        metodo_pago=datos.get("metodo_pago"),
        usuario=datos.get("usuario"),
        total=0,
        costo_total_historico=0,
        ganancia_total_historica=0
    )

    db.add(venta)
    db.flush()

    total = 0
    costo_total = 0

    for item in items:
        producto = db.query(Producto).filter(
            Producto.id == item["producto_id"],
            Producto.activo == True
        ).first()

        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        cantidad = float(item.get("cantidad", 1))

        if cantidad <= 0:
            raise HTTPException(
                status_code=400,
                detail="Cantidad inválida"
            )

        if producto.stock < cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente: {producto.nombre}"
            )

        precio = float(producto.precio_venta)
        costo = float(producto.precio_costo)

        subtotal = precio * cantidad
        costo_linea = costo * cantidad
        ganancia = subtotal - costo_linea

        margen = (
            (ganancia / subtotal) * 100
            if subtotal > 0 else 0
        )

        detalle = DetalleVenta(
            venta_id=venta.id,
            producto_id=producto.id,
            codigo_producto=producto.codigo,
            nombre_producto=producto.nombre,
            cantidad=cantidad,

            # Valores históricos congelados
            precio_venta_historico=precio,
            costo_unitario_historico=costo,

            subtotal=subtotal,
            costo_total_historico=costo_linea,
            ganancia_historica=ganancia,
            margen_historico=margen
        )

        db.add(detalle)

        producto.stock -= cantidad

        total += subtotal
        costo_total += costo_linea

    venta.total = total
    venta.costo_total_historico = costo_total
    venta.ganancia_total_historica = (
        total - costo_total
    )

    db.commit()
    db.refresh(venta)

    return {
        "ok": True,
        "venta_id": venta.id,
        "total": venta.total,
        "ganancia": venta.ganancia_total_historica
    }
