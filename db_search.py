import mysql.connector
import json

dbconfig = {
  "host":"localhost",
  "user":"root",
  "password":"0000",
  "database":"wehelp_stage2_taipei_spot",
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(
  pool_name="mypool",
  pool_size=3,
  **dbconfig
)

cnx1 = cnxpool.get_connection()



def get_distinctMRT ():
  mycursor = cnx1.cursor()
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
  mycursor = cnx1.cursor()
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
  mycursor = cnx1.cursor()
  for MRT in MRT_List:
    count = M_C_dict[f"{MRT}"]
    sql = "INSERT INTO mrt_list(MRT_name, spot_count) values (%s, %s)"
    val = (f"{MRT}",count)
    print(f"{MRT}")
    print(count)
    mycursor.execute(sql, val)
    print(mycursor.rowcount, "record inserted in mrt_List.")
    cnx1.commit()

#create mrt_list_table    
# MRT_List= get_distinctMRT()
# print(MRT_List)
# M_C_dict = get_MRT_spot_NUM(MRT_List)
# insert_MRT_count(MRT_List, M_C_dict)


def get_MRT_ORDERBY_spot_count():
  mycursor = cnx1.cursor()
  mrt_list = []
  sql = """SELECT MRT_name, spot_count FROM mrt_list ORDER BY spot_count DESC"""
  mycursor.execute(sql)
  result = mycursor.fetchall()
  for data in result:
    mrt = data[0]
    mrt_list.append(mrt)
  print(mrt_list)
  return(mrt_list)  

def get_attraction_by_id(id):
  try:
    attraction_data={}
    mycursor = cnx1.cursor(dictionary = True)
    sql1= "select * from taipei_attraction where id = %s"
    val = (f"{id}",)
    mycursor.execute(sql1, val)
    result = mycursor.fetchall()[0]
    attraction_data["id"] = result["id"]
    attraction_data["name"] = result["name"]
    attraction_data["category"] = result["CAT"]
    attraction_data["description"] = result["description"]
    attraction_data["address"] = result["address"]
    attraction_data["transport"] = result["direction"]
    attraction_data["mrt"] = result["MRT"]
    attraction_data["lat"] = result["latitude"]
    attraction_data["lng"] = result["longitude"]
# get file
    photo_list = []
    sql2 = "select photo from photo_file where attraction_id = %s"
    mycursor.execute(sql2,val)
    result2 = mycursor.fetchall()
    for photo in result2:
      photo_list.append(photo["photo"])
    attraction_data["images"] = photo_list
    return (attraction_data)
  except:
    return None 
