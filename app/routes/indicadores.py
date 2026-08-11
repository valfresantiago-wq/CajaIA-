from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.indicadores import (
    obtener_resumen,
    obtener_indicadores_ayer,
    obtener_rentabilidad,
    productos_mas_vendidos,
    productos_stock_bajo,
)


router = APIRouter(
    prefix="/api/indicadores",
    tags=["Indicadores"]
)


@router.get("")
def indicadores(
    db: Session = Depends(get_db)
):
    ahora = datetime.now()

    inicio_mes = datetime(
        ahora.year,
        ahora.month,
        1
    )

    fin = datetime.combine(
        ahora.date(),
        datetime.max.time()
    )

    resumen = obtener_resumen(db)

    mes = obtener_rentabilidad(
        db,
        inicio_mes,
        fin
    )

    ayer = obtener_indicadores_ayer(db)

    mas_vendidos = productos_mas_vendidos(
        db,
        inicio_mes,
        fin,
        10
    )

    stock_bajo = productos_stock_bajo(db)

    return {
        "resumen": resumen,
        "mes": mes,
        "ayer": ayer,
        "productos_mas_vendidos": mas_vendidos,
        "stock_bajo": [
            {
                "id": p.id,
                "codigo": p.codigo,
                "nombre": p.nombre,
                "stock": p.stock,
                "stock_minimo": p.stock_minimo
            }
            for p in stock_bajo
        ]
    }
