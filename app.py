from typing import List, Union
from fastapi import *
from fastapi.responses import FileResponse
from pydantic import BaseModel
from db_search import get_MRT_ORDERBY_spot_count

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
async def get_attraction_from_id():
	pass
@app.get("/api/mrt")
async def get_mrt(response:Response):
	try:
			mrt_list = get_MRT_ORDERBY_spot_count()
			response_200 = {
				"data" :  mrt_list
			}
			return response_200
	except:
		error_message ={
			"error": True,
			"message": "伺服器錯誤"
		}
		return error_message