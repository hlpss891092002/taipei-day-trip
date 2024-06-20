
from typing import Union
from pydantic import BaseModel

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