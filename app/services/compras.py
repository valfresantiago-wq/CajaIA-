from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field

from app.deps import require_owner
from app.view import templates
from servicios.servicio_compras import listar_compras, listar_productos, listar_proveedores, registrar_compra

router=APIRouter(prefix="/compras",tags=["compras"])

class CompraItem(BaseModel):
    producto_id:int
    cantidad:int=Field(gt=0)
    costo:float=Field(ge=0)
class CompraIn(BaseModel):
    proveedor_id:int
    comprobante:str=""
    observaciones:str=""
    items:list[CompraItem]

@router.get("",response_class=HTMLResponse)
def compras_page(request:Request):
    user=require_owner(request)
    return templates.TemplateResponse(request,"compras.html",{"user":user,"compras":listar_compras(),"proveedores":listar_proveedores(),"productos":listar_productos(),"section":"compras"})

@router.post("/api")
def compra_api(request:Request,payload:CompraIn):
    user=require_owner(request)
    cid,numero,total=registrar_compra(user.id,payload.proveedor_id,[i.model_dump() for i in payload.items],payload.comprobante,payload.observaciones)
    return {"ok":True,"compra_id":cid,"numero":numero,"total":float(total)}
