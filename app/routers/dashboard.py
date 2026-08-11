from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["Panel"]
)


ROOT = Path(__file__).resolve().parents[2]

templates = Jinja2Templates(
    directory=str(ROOT / "app" / "templates")
)


@router.get("/")
def panel(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="panel.html",
        context={
            "usuario": None,
        }
    )
