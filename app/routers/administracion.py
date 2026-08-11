from fastapi import APIRouter


router = APIRouter(
    prefix="/administracion",
    tags=["Administración"]
)


@router.get("")
def administracion():

    return {
        "ok": True,
        "mensaje": "Módulo de administración activo"
    }
