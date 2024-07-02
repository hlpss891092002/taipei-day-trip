from fastapi import *
from fastapi.responses import  JSONResponse

router = APIRouter()

@router.post("/api/orders")
async def set_order():
  pass

@router.get("/api/orders{orderNumber}")
async def set_order(request: Request, orderNumber):
  pass