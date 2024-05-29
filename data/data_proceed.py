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
# CREATE TABLE MRT_LIS
mycursor.execute("""CREATE TABLE mrt_list(
	id BIGINT AUTO_INCREMENT,
	MRT_name varchar(255),
	spot_count int,
primary KEY (id)
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
 
def get_distinctMRT ():
  mycursor = mydb.cursor()
  MRT_List = []
  mycursor.execute("SELECT DISTINCT MRT fROM taipei_attraction ")
  result = mycursor.fetchall()
  for MRT in result:
    if MRT[0] == "None":
      continue
    else:
      MRT_List.append(MRT[0])
  return MRT_List

def get_MRT_spot_NUM(MRT_List):
  mycursor = mydb.cursor()
  M_C_dict = {}
  for MRT in MRT_List:
    sql = "SELECT COUNT(*) fROM taipei_attraction WHERE MRT = %s"
    val = (f"{MRT}",)
    mycursor.execute(sql, val)
    count_num = mycursor.fetchone()[0]
    M_C_dict[f"{MRT}"] = count_num
    # print(M_C_dict)
  return M_C_dict
    
def insert_MRT_count(MRT_List, M_C_dict):
  mycursor = mydb.cursor()
  for MRT in MRT_List:
    count = M_C_dict[f"{MRT}"]
    sql = "INSERT INTO mrt_list(MRT_name, spot_count) values (%s, %s)"
    val = (f"{MRT}",count)
    print(f"{MRT}")
    print(count)
    mycursor.execute(sql, val)
    print(mycursor.rowcount, "record inserted in mrt_List.")
    mydb.commit()

# create mrt_list_table    
MRT_List= get_distinctMRT()
print(MRT_List)
M_C_dict = get_MRT_spot_NUM(MRT_List)
insert_MRT_count(MRT_List, M_C_dict)



