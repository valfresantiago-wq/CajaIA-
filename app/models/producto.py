from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func

from app.database.db import Base


class Producto(Base):
    __tablename__ = "productos"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(100), unique=True, index=True, nullable=True)
    nombre = Column(String(255), nullable=False, index=True)

    # Stock
    stock = Column(Float, nullable=False, default=0)
    stock_minimo = Column(Float, nullable=False, default=0)

    # Precios actuales
    precio_costo = Column(Float, nullable=False, default=0)
    precio_venta = Column(Float, nullable=False, default=0)

    # Información adicional
    categoria = Column(String(150), nullable=True)
    marca = Column(String(150), nullable=True)

    # Estado
    activo = Column(Boolean, nullable=False, default=True)

    # Fechas
    creado_en = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    actualizado_en = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self):
        return (
            f"<Producto "
            f"id={self.id} "
            f"codigo={self.codigo} "
            f"nombre={self.nombre}>"
        )
