
from typing import Union
from pydantic import BaseModel, EmailStr
import datetime

class error_message(BaseModel):
	error:bool
	message: str

class one_data_response(BaseModel):
	data: Union[dict, None]

class one_line_ok_200(BaseModel):
	ok : bool

class attractions_response(BaseModel):
	nextPage: Union[int, None]
	data: list

class mrts_response(BaseModel):
	data: list

error_message_500 = error_message(
	error = True,
	message="伺服器內部錯誤"
)

error_message_403_unsigned = error_message(
	error = True,
	message="未登入系統，拒絕存取"
)

error_message_403_timeout = error_message(
	error = True,
	message="無權限，拒絕存取"
)

error_message_400 = error_message(
	error = True,
	message="景點編號不正確"
)

error_message_booking_fail = error_message(
	error = True,
	message="建立失敗，輸入不正確或其他原因"
)

ok_message_200 =  one_line_ok_200(
	ok = True
)
