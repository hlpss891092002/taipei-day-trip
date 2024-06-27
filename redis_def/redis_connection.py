import redis
import json
from typing import Union
from redis.cluster import RedisCluster
def redis_con():# build a connection between python and redis 
   try:
      redis_con = redis.Redis(host='127.0.0.1', port=6379 ,decode_responses=True)
      return redis_con
   except:
      print("connect fail")
      return

def set_attractions_data_in_redis(keyword, page, data):
  try: 
   json_data = json.dumps(data, ensure_ascii=False)
   redis_con().set(f"attractions :{keyword}, {page}", json_data, ex=360)
   print("set attractions cache in redis")
  except:
     print("set attractions cache fail")
     return 
  
def get_attractions_data_in_redis(keyword, page):
   try:
      json_data = redis_con().get(f"attractions :{keyword}, {page}")
      if json_data is None:
         return json_data
      else :
         return json.loads(json_data)
   except:
      return None

def set_attraction_data_in_redis(id, data):
   try:
      json_data = json.dumps(data, ensure_ascii=False)
      redis_con().set(f"attraction :{id}", json_data, ex=360)
      print(f"set attraction{id} cache in redis")
   except:
      print("set cache fail")
      return 

def get_attraction_data_in_redis(id):
   try:
      json_data = redis_con().get(f"attraction :{id}")
      if json_data is None:
         return json_data
      else :
         return json.loads(json_data)
   except:
      return None
   
def set_mrt_data_in_redis(data):
   try:
      json_data = json.dumps(data, ensure_ascii=False)
      redis_con().set("mrt_list", json_data, ex=360)
      print("set mrt cache in redis")
   except:
      print("set cache fail")
      return 

def get_mrt_data_in_redis():
   try:
      json_data = redis_con().get("mrt_list")
      if json_data is None:
         return json_data
      else :
         return json.loads(json_data)
   except:
      return None