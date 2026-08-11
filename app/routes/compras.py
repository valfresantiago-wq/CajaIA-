from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.producto import Producto
from app.models.compra import Compra, DetalleCompra
from app.models.historial_costo import HistorialCosto


router = APIRouter(
    prefix="/api/compras",
    tags=["Compras"]
)


@router.post("")
def registrar_compra(
    datos: dict,
    db: Session = Depends(get_db)
):
    items = datos.get("items", [])

    if not items:
        raise HTTPException(
            status_code=400,
            detail="La compra no contiene productos"
        )

    compra = Compra(
        proveedor_id=datos.get("proveedor_id"),
        numero_comprobante=datos.get(
            "numero_comprobante"
        ),
        usuario=datos.get("usuario"),
        observaciones=datos.get("observaciones"),
        total=0
    )

    db.add(compra)
    db.flush()

    total_compra = 0

    for item in items:
        producto = db.query(Producto).filter(
            Producto.id == item["producto_id"]
        ).first()

        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        cantidad = float(item["cantidad"])
        costo_nuevo = float(item["costo_unitario"])

        if cantidad <= 0 or costo_nuevo < 0:
            raise HTTPException(
                status_code=400,
                detail="Datos de compra inválidos"
            )

        costo_anterior = float(
            producto.precio_costo or 0
        )

        subtotal = cantidad * costo_nuevo

        detalle = DetalleCompra(
            compra_id=compra.id,
            producto_id=producto.id,
            codigo_producto=producto.codigo,
            nombre_producto=producto.nombre,
            cantidad=cantidad,
            costo_unitario=costo_nuevo,
            costo_anterior=costo_anterior,
            subtotal=subtotal
        )

        db.add(detalle)

        # Ingreso físico de mercadería
        producto.stock += cantidad

        # Nuevo costo vigente
        producto.precio_costo = costo_nuevo

        diferencia = costo_nuevo - costo_anterior

        porcentaje = 0

        if costo_anterior > 0:
            porcentaje = (
                diferencia / costo_anterior
            ) * 100

        historial = HistorialCosto(
            producto_id=producto.id,
            compra_id=compra.id,
            costo_anterior=costo_anterior,
            costo_nuevo=costo_nuevo,
            diferencia=diferencia,
            porcentaje_variacion=porcentaje,
            motivo="Compra"
        )

        db.add(historial)

        total_compra += subtotal

    compra.total = total_compra

    db.commit()
    db.refresh(compra)

    return {
        "ok": True,
        "compra_id": compra.id,
        "total": compra.total
    }
