from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/indicadores",
    tags=["Indicadores"]
)


ROOT = Path(__file__).resolve().parents[2]

templates = Jinja2Templates(
    directory=str(ROOT / "app" / "templates")
)


@router.get("")
def pagina_indicadores(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="indicadores.html",
        context={
            "usuario": None,
        }
    )
