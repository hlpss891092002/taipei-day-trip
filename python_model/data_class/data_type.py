
from typing import Union
from pydantic import BaseModel, EmailStr
import datetime

class signup_data(BaseModel):
	name: str
	email: EmailStr
	password: str

class booking_order(BaseModel):
	attractionId: int
	date: datetime.date
	time: str
	price: int


class signin_data(BaseModel):
	email: EmailStr
	password: str