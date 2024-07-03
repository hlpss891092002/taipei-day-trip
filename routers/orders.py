import jwt
import requests
from fastapi import APIRouter, Depends, Request
from fastapi.responses import  JSONResponse
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from datetime import *
from starlette import status
from python_model.data_class.data_type import *
from python_model.data_class.response_classes import *
from python_model.db.orders_method import *

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/api/orders")
async def set_order(body: order_data,  token : Annotated[str, Depends(oauth2_scheme)]):
  try :
    if(token):
      now = datetime.now().strftime('%Y%m%d')
      decode_JWT = jwt.decode(token , os.getenv("JWTSECRET"), algorithms=["HS256"])
      prime = body.prime
      member_id = decode_JWT["iss"]
      contact = body.contact
      order = body.order
      order_id = insert_order_table( member_id, contact, order)
      if order_id:
        TPC_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"

        cardholder = {
          "phone_number" : body.contact.phone,
          "name": body.contact.name,
          "email": body.contact.email
        }

        headers = {
        "Content-Type": "application/json",
          "x-api-key": "partner_1PQMggjgJHM5bZ6CfgGcUstjSgbzCCfxKR9gPFsSjT5L5VLGGmVMbChZ"    
        }

        payload = {
          "prime" : prime,
          "partner_key": "partner_1PQMggjgJHM5bZ6CfgGcUstjSgbzCCfxKR9gPFsSjT5L5VLGGmVMbChZ",
          "merchant_id": "hlpss891092002_FUBON_POS_1",
          "details":"TapPay Test",
          "amount": body.order.price,
          "cardholder": cardholder
        }

        TPCresponse = requests.post(TPC_url, json = payload, headers= headers).json()
        # print(TPCresponse.json())
        msg = TPCresponse["msg"]
        if msg == "Success":
          data =  {
            "number": order_id,
            "payment": {
              "status": TPCresponse["status"],
              "message": "付款成功"
            }
          }
          pay_success= order_response(
            data = data
          )
          turn_to_paid(order_id)
          print(pay_success)
          return pay_success
        else:
          data =  {
            "number": order_id,
            "payment": {
              "status": TPCresponse["status"],
              "message": "付款失敗"
            }
          }
          pay_fail = order_response(
            data = data
          )
          return pay_fail
      else:
        print("order fail")
        return JSONResponse(status_code=400, content=error_message_order_fail.dict())
    else:
      return JSONResponse(status_code=403, content=error_message_403_unsigned.dict())
  except Exception as e:
    print(f" error in order.py on {e}")
    return JSONResponse(status_code=500, content=error_message_500.dict())


@router.get("/api/orders/{orderNumber}")
async def set_order(request: Request, orderNumber, token : Annotated[str, Depends(oauth2_scheme)]):
  try :
      if(token):
        print(orderNumber)
        order_data = getOrderData(orderNumber)
        return order_data
      else:
        return JSONResponse(status_code=403, content=error_message_403_unsigned.dict())
  except Exception as e:
    print(f" error in order.py on {e}")
    return JSONResponse(status_code=500, content=error_message_500.dict())