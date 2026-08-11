from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.producto import Producto
from app.models.venta import Venta, DetalleVenta
from app.models.compra import Compra


# =========================================================
# RESUMEN GENERAL
# =========================================================

def obtener_resumen(db: Session):

    total_productos = (
        db.query(func.count(Producto.id))
        .filter(Producto.activo == True)
        .scalar()
        or 0
    )

    stock_total = (
        db.query(func.sum(Producto.stock))
        .filter(Producto.activo == True)
        .scalar()
        or 0
    )

    valor_stock_costo = (
        db.query(
            func.sum(
                Producto.stock * Producto.precio_costo
            )
        )
        .filter(Producto.activo == True)
        .scalar()
        or 0
    )

    valor_stock_venta = (
        db.query(
            func.sum(
                Producto.stock * Producto.precio_venta
            )
        )
        .filter(Producto.activo == True)
        .scalar()
        or 0
    )

    return {
        "total_productos": total_productos,
        "stock_total": stock_total,
        "valor_stock_costo": valor_stock_costo,
        "valor_stock_venta": valor_stock_venta,
    }


# =========================================================
# RENTABILIDAD POR PERÍODO
# =========================================================

def obtener_rentabilidad(
    db: Session,
    fecha_desde: datetime,
    fecha_hasta: datetime
):

    resultado = (
        db.query(
            func.sum(Venta.total),
            func.sum(Venta.costo_total_historico),
            func.sum(Venta.ganancia_total_historica)
        )
        .filter(
            Venta.fecha >= fecha_desde,
            Venta.fecha <= fecha_hasta
        )
        .first()
    )

    ventas = resultado[0] or 0
    costos = resultado[1] or 0
    ganancia = resultado[2] or 0

    margen = 0

    if ventas > 0:
        margen = (ganancia / ventas) * 100

    return {
        "ventas": ventas,
        "costos": costos,
        "ganancia": ganancia,
        "margen": margen
    }


# =========================================================
# INDICADORES DE AYER
# =========================================================

def obtener_indicadores_ayer(db: Session):

    hoy = datetime.now().date()
    ayer = hoy - timedelta(days=1)

    inicio = datetime.combine(
        ayer,
        datetime.min.time()
    )

    fin = datetime.combine(
        ayer,
        datetime.max.time()
    )

    return obtener_rentabilidad(
        db,
        inicio,
        fin
    )


# =========================================================
# PRODUCTOS MÁS VENDIDOS
# =========================================================

def productos_mas_vendidos(
    db: Session,
    fecha_desde: datetime,
    fecha_hasta: datetime,
    limite: int = 10
):

    resultados = (
        db.query(
            DetalleVenta.producto_id,
            DetalleVenta.nombre_producto,
            func.sum(DetalleVenta.cantidad).label("cantidad"),
            func.sum(DetalleVenta.subtotal).label("facturacion"),
            func.sum(
                DetalleVenta.ganancia_historica
            ).label("ganancia")
        )
        .join(
            Venta,
            DetalleVenta.venta_id == Venta.id
        )
        .filter(
            Venta.fecha >= fecha_desde,
            Venta.fecha <= fecha_hasta
        )
        .group_by(
            DetalleVenta.producto_id,
            DetalleVenta.nombre_producto
        )
        .order_by(
            func.sum(DetalleVenta.cantidad).desc()
        )
        .limit(limite)
        .all()
    )

    return [
        {
            "producto_id": r.producto_id,
            "producto": r.nombre_producto,
            "cantidad": r.cantidad or 0,
            "facturacion": r.facturacion or 0,
            "ganancia": r.ganancia or 0
        }
        for r in resultados
    ]


# =========================================================
# PRODUCTOS CON STOCK BAJO
# =========================================================

def productos_stock_bajo(db: Session):

    productos = (
        db.query(Producto)
        .filter(
            Producto.activo == True,
            Producto.stock <= Producto.stock_minimo
        )
        .order_by(Producto.stock.asc())
        .all()
    )

    return productos


# =========================================================
# COMPRAS POR PERÍODO
# =========================================================

def total_compras(
    db: Session,
    fecha_desde: datetime,
    fecha_hasta: datetime
):

    total = (
        db.query(func.sum(Compra.total))
        .filter(
            Compra.fecha >= fecha_desde,
            Compra.fecha <= fecha_hasta
        )
        .scalar()
        or 0
    )

    return total
