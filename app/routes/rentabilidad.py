from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.indicadores import obtener_rentabilidad


router = APIRouter(
    prefix="/api/rentabilidad",
    tags=["Rentabilidad"]
)


@router.get("")
def rentabilidad(
    desde: str | None = None,
    hasta: str | None = None,
    periodo: str | None = None,
    db: Session = Depends(get_db)
):
    ahora = datetime.now()

    if periodo == "hoy":
        fecha_desde = datetime.combine(
            ahora.date(),
            datetime.min.time()
        )

        fecha_hasta = datetime.combine(
            ahora.date(),
            datetime.max.time()
        )

    elif periodo == "ayer":
        ayer = ahora.date() - timedelta(days=1)

        fecha_desde = datetime.combine(
            ayer,
            datetime.min.time()
        )

        fecha_hasta = datetime.combine(
            ayer,
            datetime.max.time()
        )

    elif periodo == "semana":
        inicio_semana = (
            ahora.date()
            - timedelta(days=ahora.weekday())
        )

        fecha_desde = datetime.combine(
            inicio_semana,
            datetime.min.time()
        )

        fecha_hasta = agora_fin = datetime.combine(
            ahora.date(),
            datetime.max.time()
        )

    elif periodo == "mes":
        inicio_mes = agora_inicio = agora_date = agora = None
        fecha_desde = datetime(
            ahora.year,
            ahora.month,
            1
        )

        fecha_hasta = datetime.combine(
            ahora.date(),
            datetime.max.time()
        )

    else:
        if desde:
            fecha_desde = datetime.strptime(
                desde,
                "%Y-%m-%d"
            )
        else:
            fecha_desde = datetime.combine(
                ahora.date(),
                datetime.min.time()
            )

        if hasta:
            fecha_hasta = datetime.combine(
                datetime.strptime(
                    hasta,
                    "%Y-%m-%d"
                ).date(),
                datetime.max.time()
            )
        else:
            fecha_hasta = datetime.combine(
                fecha_desde.date(),
                datetime.max.time()
            )

    resultado = obtener_rentabilidad(
        db,
        fecha_desde,
        fecha_hasta
    )

    return {
        "desde": fecha_desde,
        "hasta": fecha_hasta,
        **resultado
    }
