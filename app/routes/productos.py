from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.producto import Producto


router = APIRouter(
    prefix="/api/productos",
    tags=["Productos"]
)


@router.get("")
def listar_productos(
    buscar: str | None = None,
    db: Session = Depends(get_db)
):
    consulta = db.query(Producto).filter(
        Producto.activo == True
    )

    if buscar:
        termino = f"%{buscar}%"

        consulta = consulta.filter(
            (Producto.nombre.ilike(termino)) |
            (Producto.codigo.ilike(termino)) |
            (Producto.marca.ilike(termino))
        )

    return consulta.order_by(
        Producto.nombre.asc()
    ).all()


@router.get("/{producto_id}")
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    producto = db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.activo == True
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto
