import mysql.connector
import json

# load in db
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "0000",
  database = "wehelp_stage2_taipei_spot",
)
  
mycursor = mydb.cursor()

mycursor.execute("""""")

def insert_value_in_taipei_table(spot):
  name = spot["name"]
  MRT = spot["MRT"]
  address = spot["address"]
  rate = spot["rate"]
  direction = spot["direction"]
  description = spot["description"]
  CAT = spot["CAT"]
  MEMO_TIME = spot["MEMO_TIME"]
  longitude = spot["longitude"]
  latitude = spot["latitude"]
  sql = "INSERT INTO taipei_attraction(name, MRT, address, rate, direction, description, CAT, MEMO_TIME, longitude, latitude) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
  val = (f"{name}", f"{MRT}", f"{address}", rate, f"{direction}", f"{description}", f"{CAT}", f"{MEMO_TIME}", longitude, latitude )
  mycursor.execute(sql, val)
  mydb.commit()
  print(mycursor.rowcount, "record inserted in taipei_attraction.")

def file_list(spot):
  data = spot["file"].split("http")
  photo_list = []
  for info in data:
    info = "http"+ info
    if info.endswith("JPG") or  info.endswith("jpg") or  info.endswith("png") or info.endswith("PNG") :
      photo_list.append(info)
  return photo_list

def insert_value_in_photo(count, photo_list):
  for photo in photo_list:
    sql = """INSERT INTO photo_file(attraction_id, photo) VALUES(%s, %s)"""
    val = (count, f"{photo}")
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted in photo_file.")


# # load json data
with open("taipei-attractions.json", encoding='utf8') as f:
  data = json.load(f)
all_data = data["result"]["results"]
count = 1
for spot in all_data:
  insert_value_in_taipei_table(spot) # insert taipei_table 
  photo_list = file_list(spot)
  insert_value_in_photo(count, photo_list) #insert photo_file
  print(count)
  print(photo_list)
  count+=1
 



