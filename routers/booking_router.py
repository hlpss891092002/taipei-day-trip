import jwt
from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from datetime import *
from python_model.db.member_data_method import *
from python_model.data_class.response_classes import *
from python_model.db.booking_method import*
from python_model.data_class.data_type import *


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/api/booking")
async def get_booking(request:Request, token : Annotated[str, Depends(oauth2_scheme)]):
  try:
    if (token):
      now = int((datetime.datetime.now()).timestamp())
      decode_JWT = jwt.decode(token , os.getenv("JWTSECRET"), algorithms=["HS256"])
      if now > decode_JWT["exp"]:
        print("Authorization timeout")
        return JSONResponse(status_code=403, content=error_message_403_timeout.model_dump())
      else:
        member_id = decode_JWT["iss"]
        responses_200 = one_data_response(
          data = render_booking_order(member_id)
        )
        return responses_200
    else:
      return JSONResponse(status_code=403, content=error_message_403_unsigned.model_dump())
  except:
      return JSONResponse(status_code=500, content=error_message_500.model_dump())

@router.post("/api/booking")
async def get_booking(request: Request, body:booking_order, token : Annotated[str, Depends(oauth2_scheme)]):
  try:
    if (token):
      now = int((datetime.datetime.now()).timestamp())
      decode_JWT = jwt.decode(token , os.getenv("JWTSECRET"), algorithms=["HS256"])
      if now > decode_JWT["exp"]:
        print("Authorization timeout")
        return JSONResponse(status_code=403, content=error_message_403_timeout.model_dump())
      else:
        member_id = decode_JWT["iss"]
        if (insert_booking_order(member_id, body.attractionId, body.date, body.time, body.price)):
          return JSONResponse(status_code=200, content=ok_message_200.model_dump())
        else: 
          return  JSONResponse(status_code=400, content=error_message_booking_fail.model_dump())
    else:
      return JSONResponse(status_code=403, content=error_message_403_unsigned.model_dump())
  except:
      return JSONResponse(status_code=500, content=error_message_500.model_dump())
  

@router.delete("/api/booking")
async def get_booking(request:Request, token : Annotated[str, Depends(oauth2_scheme)]):
    try:
      if (token):
        now = int((datetime.datetime.now()).timestamp())
        decode_JWT = jwt.decode(token , os.getenv("JWTSECRET"), algorithms=["HS256"])
        if now > decode_JWT["exp"]:
          print("Authorization timeout")
          return JSONResponse(status_code=403, content=error_message_403_timeout.model_dump())
        else:
          member_id = decode_JWT["iss"]
          if (delete_booking(member_id)):
           return ok_message_200 
      else:
        return JSONResponse(status_code=403, content=error_message_403_unsigned.model_dump())
    except:
        return JSONResponse(status_code=500, content=error_message_500.model_dump())
    
    