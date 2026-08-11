from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(
        String(255),
        nullable=False,
        index=True
    )

    telefono = Column(String(100), nullable=True)
    whatsapp = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)

    direccion = Column(String(255), nullable=True)
    localidad = Column(String(150), nullable=True)

    observaciones = Column(String(500), nullable=True)

    activo = Column(
        Boolean,
        nullable=False,
        default=True
    )

    creado_en = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    compras = relationship(
        "Compra",
        back_populates="proveedor"
    )
