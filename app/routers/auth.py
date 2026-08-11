from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)


@router.get("/login")
def login():
    return {
        "ok": True,
        "mensaje": "Módulo de autenticación activo"
    }


@router.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )
