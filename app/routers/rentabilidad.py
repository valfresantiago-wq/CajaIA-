from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/rentabilidad",
    tags=["Rentabilidad"]
)


ROOT = Path(__file__).resolve().parents[2]

templates = Jinja2Templates(
    directory=str(ROOT / "app" / "templates")
)


@router.get("")
def pagina_rentabilidad(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="rentabilidad.html",
        context={
            "usuario": None,
        }
    )
