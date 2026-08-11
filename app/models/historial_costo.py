from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class HistorialCosto(Base):
    __tablename__ = "historial_costos"

    id = Column(Integer, primary_key=True, index=True)

    producto_id = Column(
        Integer,
        ForeignKey("productos.id"),
        nullable=False,
        index=True
    )

    compra_id = Column(
        Integer,
        ForeignKey("compras.id"),
        nullable=True,
        index=True
    )

    fecha = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        index=True
    )

    costo_anterior = Column(
        Float,
        nullable=True
    )

    costo_nuevo = Column(
        Float,
        nullable=False
    )

    diferencia = Column(
        Float,
        nullable=False,
        default=0
    )

    porcentaje_variacion = Column(
        Float,
        nullable=False,
        default=0
    )

    motivo = Column(
        String(255),
        nullable=True
    )

    producto = relationship("Producto")
    compra = relationship("Compra")
