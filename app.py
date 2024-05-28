from typing import List, Union
from fastapi import *
from fastapi.responses import FileResponse, ORJSONResponse
from pydantic import BaseModel
from db_search import get_MRT_ORDERBY_spot_count, get_attraction_by_id

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
async def get_attraction():
	pass
@app.get("/api/attraction/{attractionId}")
async def get_attraction_from_id(attractionId):
	try:
		data = get_attraction_by_id(attractionId)
		if data is None:
			return ORJSONResponse(status_code=400, content={"error":True, "message":"景點編號不正確"})
		else :
			response_200 = {}
			response_200["data"] = data 
			return 	response_200
	except:
		error_message ={
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return ORJSONResponse(status_code=500, content=error_message)
@app.get("/api/mrt")
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
		return error_message