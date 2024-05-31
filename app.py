from typing import List, Union
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from db_search import get_MRT_ORDERBY_spot_count, get_attraction_by_id, get_attraction_by_keyword_page

class error_message(BaseModel):
	error:bool
	message: str

class attractionId_response(BaseModel):
	data: dict

class mrts_response(BaseModel):
	data: list

error_message_500 = error_message(
	error = True,
	message="伺服器內部錯誤"
)

error_message_400 = error_message(
	error = True,
	message="景點編號不正確"
)

app= FastAPI()


# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

# edit from here
@app.get("/api/attractions")
async def get_attraction(keyword: str = None, page: int = 0):
	try:
		return  get_attraction_by_keyword_page(keyword, page)
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())
@app.get("/api/attraction/{attractionId}")
async def get_attraction_from_id(attractionId):
	try:
		attraction_id_data = get_attraction_by_id(attractionId)
		if attraction_id_data is None:
			return JSONResponse(status_code=400, content=error_message_400.dict())
		else :
			response_200 = attractionId_response(
				data = attraction_id_data
			) 
			return 	response_200.dict()
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())
@app.get("/api/mrts")
async def get_mrt():
	try:
			response_200 = mrts_response(
				data = get_MRT_ORDERBY_spot_count()
			)
			return response_200.dict()
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())