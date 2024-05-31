import mysql.connector
import json

mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "00000000",
)
mycursor1 = mydb.cursor()
#create db 
mycursor1.execute("""CREATE DATABASE wehelp_stage2_taipei_spot""")

# load in db
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "00000000",
  database = "wehelp_stage2_taipei_spot",
)
  
mycursor = mydb.cursor()


#create TABLE taipei_attraction
mycursor.execute("""CREATE TABLE taipei_attraction(
                    id BIGINT AUTO_INCREMENT,
                    name varchar(255),
                    MRT varchar(255),
                    address varchar(255),
                    rate int,
                    direction varchar(2000),
                    description varchar(2000),
                    CAT varchar(255),
                    MEMO_TIME varchar(500),
                    longitude float,
                    latitude float,
                    primary key(id)
)""")
#create TABLE photo_file
mycursor.execute("""CREATE TABLE photo_file(
                 id BIGINT AUTO_INCREMENT,
                 attraction_id BIGINT,
                 photo varchar(500),
                 PRIMARY KEY(id),
                 FOREIGN KEY photo_file(attraction_id) 	REFERENCES taipei_attraction(id)
)""")



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

def get_id (spot):
  name = spot["name"]
  sql = "SELECT id FROM  taipei_attraction WHERE name =%s"
  val = (name, )
  mycursor.execute(sql, val)
  id = mycursor.fetchone()[0]
  print(id)

def insert_value_in_photo(id, photo_list):
  for photo in photo_list:
    sql = """INSERT INTO photo_file(attraction_id, photo) VALUES(%s, %s)"""
    val = (id, f"{photo}")
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted in photo_file.")


# # load json data
with open("taipei-attractions.json", encoding='utf8') as f:
  data = json.load(f)
all_data = data["result"]["results"]
for spot in all_data:
  insert_value_in_taipei_table(spot) # insert taipei_table 
  photo_list = file_list(spot)
  id = get_id (spot)
  insert_value_in_photo(id, photo_list) #insert photo_file



