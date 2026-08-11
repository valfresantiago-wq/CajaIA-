from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)

    fecha = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        index=True
    )

    total = Column(Float, nullable=False, default=0)
    costo_total_historico = Column(Float, nullable=False, default=0)
    ganancia_total_historica = Column(Float, nullable=False, default=0)

    metodo_pago = Column(String(100), nullable=True)
    usuario = Column(String(150), nullable=True)

    detalles = relationship(
        "DetalleVenta",
        back_populates="venta",
        cascade="all, delete-orphan"
    )


class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, index=True)

    venta_id = Column(
        Integer,
        ForeignKey("ventas.id"),
        nullable=False,
        index=True
    )

    producto_id = Column(
        Integer,
        ForeignKey("productos.id"),
        nullable=False,
        index=True
    )

    # Fotografía histórica del producto
    codigo_producto = Column(String(100), nullable=True)
    nombre_producto = Column(String(255), nullable=False)

    cantidad = Column(Float, nullable=False, default=1)

    # Valores congelados al momento de vender
    precio_venta_historico = Column(Float, nullable=False, default=0)
    costo_unitario_historico = Column(Float, nullable=False, default=0)

    subtotal = Column(Float, nullable=False, default=0)
    costo_total_historico = Column(Float, nullable=False, default=0)
    ganancia_historica = Column(Float, nullable=False, default=0)
    margen_historico = Column(Float, nullable=False, default=0)

    venta = relationship(
        "Venta",
        back_populates="detalles"
    )

    producto = relationship("Producto")
