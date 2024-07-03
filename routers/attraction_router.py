import json
from fastapi import *
from fastapi.responses import  JSONResponse
from python_model.db.attraction_db_method import *
from python_model.data_class.response_classes import *
from redis_def.redis_connection import *
from python_model.data_class.response_classes import *


router = APIRouter()

@router.get("/api/attractions")
async def get_attraction(keyword: str = None, page: int = 0):
	cache_data = get_attractions_data_in_redis(keyword, page)
	try:
		if cache_data is None :
			data = get_attraction_by_keyword_page(keyword, page)
			set_attractions_data_in_redis(keyword, page, data)
		else:
			print("get attraction from cache")
			data = get_attractions_data_in_redis(keyword, page)
		attractions_200 = attractions_response(
			nextPage = data["nextPage"],
			data= data["data"]
		)
		return attractions_200
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())
	
@router.get("/api/attraction/{attractionId}")
async def get_attraction_from_id(attractionId):
	cache_data = get_attraction_data_in_redis(attractionId)
	try:
		if cache_data is None:
			attraction_id_data = get_attraction_by_id(attractionId)
			if attraction_id_data is None:
				set_attraction_data_in_redis(attractionId, attraction_id_data)
				return JSONResponse(status_code=400, content=error_message_400.dict())
			else :
				response_200 = one_data_response(
					data = attraction_id_data
				)
				set_attraction_data_in_redis(attractionId, attraction_id_data) 
				return 	response_200.dict()
		else :
			print(f"get attraction{attractionId}  from cache")
			response_200 = one_data_response(
					data = cache_data
			)
			return 	response_200.dict()
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())

@router.get("/api/mrts")
async def get_mrt():
	cache_data = get_mrt_data_in_redis()
	try:
			if cache_data is None:
				response_200 = mrts_response(
					data = get_MRT_ORDERBY_spot_count()
				)
				set_mrt_data_in_redis(get_MRT_ORDERBY_spot_count())
				return response_200.dict()
			else :
				print("get mrts from cache")
				response_200 = mrts_response(
					data = cache_data
				)
				return response_200.dict()
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())
	