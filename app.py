from typing import List, Union
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from db_search import get_MRT_ORDERBY_spot_count, get_attraction_by_id, get_attraction_by_keyword_page

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
@app.get("/api/attractions")
async def get_attraction(keyword: str = None, page: int = 0):
	try:
		return  get_attraction_by_keyword_page(keyword, page)
	except:
		error_message ={
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return JSONResponse(status_code=500, content=error_message)
@app.get("/api/attraction/{attractionId}")
async def get_attraction_from_id(attractionId):
	try:
		data = get_attraction_by_id(attractionId)
		if data is None:
			return JSONResponse(status_code=400, content={"error":True, "message":"景點編號不正確"})
		else :
			response_200 = {}
			response_200["data"] = data 
			return 	response_200
	except:
		error_message ={
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return JSONResponse(status_code=500, content=error_message)
@app.get("/api/mrts")
async def get_mrt():
	try:
			mrt_list = get_MRT_ORDERBY_spot_count()
			response_200 = {
				"data" :  mrt_list
			}
			return response_200
	except:
		error_message ={
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return JSONResponse(status_code=500, content=error_message)