from fastapi import *
from fastapi.responses import  JSONResponse
from model.attraction_db_method import *
from view.response_classes import *

router = APIRouter()

@router.get("/api/attractions")
async def get_attraction(keyword: str = None, page: int = 0):
	try:
		data = get_attraction_by_keyword_page(keyword, page)
		attractions_200 = attractions_response(
			nextPage = data["nextPage"],
			data= data["data"]
		)
		return attractions_200
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())
	
@router.get("/api/attraction/{attractionId}")
async def get_attraction_from_id(attractionId):
	try:
		attraction_id_data = get_attraction_by_id(attractionId)
		if attraction_id_data is None:
			return JSONResponse(status_code=400, content=error_message_400.dict())
		else :
			response_200 = one_data_response(
				data = attraction_id_data
			) 
			return 	response_200.dict()
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())


@router.get("/api/mrts")
async def get_mrt():
	try:
			response_200 = mrts_response(
				data = get_MRT_ORDERBY_spot_count()
			)
			return response_200.dict()
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())
	