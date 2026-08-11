from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/compras",
    tags=["Compras"]
)


ROOT = Path(__file__).resolve().parents[2]

templates = Jinja2Templates(
    directory=str(ROOT / "app" / "templates")
)


@router.get("")
def pagina_compras(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="compras.html",
        context={
            "usuario": None,
        }
    )
