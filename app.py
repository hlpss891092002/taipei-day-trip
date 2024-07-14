import logging
import sys
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from python_model.db.attraction_db_method import *
from python_model.data_class.response_classes import *
from routers import attraction_router, user_router, booking_router, orders

logger = logging.getLogger(__name__)
Format = ' %(asctime)s - %(message)s'
logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO, format=Format)

class LogRequestMiddleware(BaseHTTPMiddleware):
		async def dispatch(self, request:Request, call_next):
				logger.info(f"IP : {request.client.host}, method : {request.method},  to URL: {request.url.path}'")
				response = await call_next(request)
				return response

app= FastAPI()
app.include_router(attraction_router.router)
app.include_router(user_router.router)
app.include_router(booking_router.router)
app.include_router(orders.router)
app.add_middleware(LogRequestMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")



# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction_router(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

# edit from here

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
				content=jsonable_encoder({
					"error": True,
					"message": f"type: {exc.errors()[0]['msg']}, loction: {exc.errors()[0]['loc']}"}),
    )

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
# 		print(f"OMG! An HTTP error!: {repr(exc)}")
# 		return await http_exception_handler(request, exc)
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "error": True,
#             "message": str(exc.detail)
#         }
# 			)