import logging
import jwt
from datetime import *
from typing import List, Union
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_search import *
from db_process import member_data_method 

secret = "nwzTHwTX2S7cZNXET2DSDvkFYHfVFFdb"

class error_message(BaseModel):
	error:bool
	message: str

class one_data_response(BaseModel):
	data: Union[dict, None]

class attractions_response(BaseModel):
	nextPage: Union[int, None]
	data: list

class signup_data(BaseModel):
	name: str
	email: str
	password: str

class signin_data(BaseModel):
	email: str
	password: str

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


app.mount("/static", StaticFiles(directory="static"), name="static")

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
		nextPage = check_next_page_empty(keyword, page)
		data = get_attraction_by_keyword_page(keyword, page)
		attractions_200 = attractions_response(
			nextPage = nextPage,
			data= data
		)
		return attractions_200
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())
	
@app.get("/api/attraction/{attractionId}")
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

@app.get("/api/mrts")
async def get_mrt():
	try:
			response_200 = mrts_response(
				data = get_MRT_ORDERBY_spot_count()
			)
			return response_200.dict()
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())
	
@app.post("/api/user")
async def sign_up_member(body: signup_data):
	try:
		result = member_data_method.add_member(body.name, body.email, body.password)
		if result == True:
			sign_up_success = {
				"ok" : True
			}
			return sign_up_success
		else:
			error_message_signup_fail = error_message(
				error = True,
				message = result
			)
			return JSONResponse(status_code=400, content=error_message_signup_fail.dict())
	except:
		return JSONResponse(status_code=500, content=error_message_500.dict())
		
@app.get("/api/user/auth")
async def get_user_auth(request :Request):
	try:
		token = request.headers["Authorization"].split()[1]
		decode_JWT = jwt.decode(token , "secret", algorithms=["HS256"])
		member_data = member_data_method.check_member(decode_JWT["iss"], decode_JWT["email"],)
		responses_body = one_data_response(
			data = member_data
		)
		return responses_body
	except:
		responses_body = one_data_response(
			data = None
		)
		return responses_body

@app.put("/api/user/auth")
async def sign_in(body: signin_data):
	try:
		member_data =  member_data_method.signin(body.email,body.password)
		if member_data:
			payload = {
				"iss" : member_data["id"],
				"email" : member_data["email"],
				"exp": datetime.now() + timedelta(weeks=1)
				}
			token = jwt.encode(payload, "secret", algorithm="HS256")
			response_token = {
				"token" : token
			}
			return response_token
		else:
			error_message_signup_fail = error_message(
				error = True,
				message = "登入失敗，電子郵件或密碼錯誤或其他原因"
			)
			return JSONResponse(status_code=400, content=error_message_signup_fail.dict())
	except:
				return JSONResponse(status_code=500, content=error_message_500.dict())
