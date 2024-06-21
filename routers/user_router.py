import jwt
from fastapi import *
from fastapi.responses import JSONResponse
from datetime import *
from  db.member_data_method import *
from data_class.response_classes import *


router = APIRouter()

@router.post("/api/user")
async def sign_up_member(body: signup_data):
	try:
		result = add_member(body.name, body.email, body.password)
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
		
@router.get("/api/user/auth")
async def get_user_auth(request :Request):
	try:
		token = request.headers["Authorization"].split()[1]
		decode_JWT = jwt.decode(token , os.getenv("JWTSECRET"), algorithms=["HS256"])
		member_data = check_member(decode_JWT["iss"], decode_JWT["email"],)
		responses_body = one_data_response(
			data = member_data
		)
		return responses_body
	except:
		responses_body = one_data_response(
			data = None
		)
		return responses_body

@router.put("/api/user/auth")
async def sign_in(body: signin_data):
	try:
		member_data =  signin(body.email,body.password)
		if member_data:
			payload = {
				"iss" : member_data["id"],
				"email" : member_data["email"],
				"exp": datetime.now() + timedelta(weeks=1)
				}
			token = jwt.encode(payload, os.getenv("JWTSECRET"), algorithm="HS256")
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

