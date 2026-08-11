from fastapi import APIRouter


router = APIRouter(
    prefix="/catalogo",
    tags=["Catálogo"]
)


@router.get("")
def catalogo():

    return {
        "ok": True,
        "mensaje": "Catálogo Libreya activo"
    }
