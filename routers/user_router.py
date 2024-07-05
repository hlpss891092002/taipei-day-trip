import jwt
from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from datetime import datetime, timedelta
from python_model.db.member_data_method import *
from python_model.data_class.response_classes import *
from redis_def.redis_connection import *
from python_model.data_class.data_type import *

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
async def get_user_auth(token : Annotated[str, Depends(oauth2_scheme)]):
	try:
		decode_JWT = jwt.decode(token , os.getenv("JWTSECRET"), algorithms=["HS256"])
		now = int((datetime.datetime.now()).timestamp())
		if now > decode_JWT["exp"]:
			responses_body = one_data_response(
				data = None
			)
			print("Authorization timeout")
			return responses_body
		else:
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
				"exp": datetime.datetime.now() + timedelta(days=1)
				}
			print(payload["exp"])
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

