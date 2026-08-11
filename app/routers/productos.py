from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["Productos"]
)


ROOT = Path(__file__).resolve().parents[2]

templates = Jinja2Templates(
    directory=str(ROOT / "app" / "templates")
)


@router.get("/stock")
def pagina_stock(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="stock.html",
        context={
            "usuario": None,
        }
    )


@router.get("/api/productos")
def api_productos():

    return {
        "ok": True,
        "productos": []
    }
