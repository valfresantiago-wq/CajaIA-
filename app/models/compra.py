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


class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, index=True)

    proveedor_id = Column(
        Integer,
        ForeignKey("proveedores.id"),
        nullable=True,
        index=True
    )

    fecha = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        index=True
    )

    numero_comprobante = Column(
        String(150),
        nullable=True
    )

    total = Column(
        Float,
        nullable=False,
        default=0
    )

    usuario = Column(
        String(150),
        nullable=True
    )

    observaciones = Column(
        String(500),
        nullable=True
    )

    proveedor = relationship(
        "Proveedor",
        back_populates="compras"
    )

    detalles = relationship(
        "DetalleCompra",
        back_populates="compra",
        cascade="all, delete-orphan"
    )


class DetalleCompra(Base):
    __tablename__ = "detalle_compras"

    id = Column(Integer, primary_key=True, index=True)

    compra_id = Column(
        Integer,
        ForeignKey("compras.id"),
        nullable=False,
        index=True
    )

    producto_id = Column(
        Integer,
        ForeignKey("productos.id"),
        nullable=False,
        index=True
    )

    codigo_producto = Column(
        String(100),
        nullable=True
    )

    nombre_producto = Column(
        String(255),
        nullable=False
    )

    cantidad = Column(
        Float,
        nullable=False,
        default=0
    )

    costo_unitario = Column(
        Float,
        nullable=False,
        default=0
    )

    costo_anterior = Column(
        Float,
        nullable=True
    )

    subtotal = Column(
        Float,
        nullable=False,
        default=0
    )

    compra = relationship(
        "Compra",
        back_populates="detalles"
    )

    producto = relationship("Producto")
