
from typing import Union
from pydantic import BaseModel, EmailStr, Field
import datetime
import re

phone_pattern = r"^09\d{8}"

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

class order_trip_attraction(BaseModel):
	id : int
	name :str
	address: str
	image : str

class order_trip(BaseModel):
	attraction : order_trip_attraction

class order_order(BaseModel):
	price : int
	trip : order_trip
	date: datetime.date
	time: str

class order_contact(BaseModel):
	name : str
	email : EmailStr
	phone : str = Field(..., pattern = phone_pattern)

class order_data(BaseModel):
	prime : str
	order : order_order
	contact: order_contact