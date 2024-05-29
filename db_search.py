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

def get_images (id):
  mycursor = cnx1.cursor(dictionary = True)
  photo_list = []
  sql = "select photo from photo_file where attraction_id = %s"
  val = (id, )
  mycursor.execute(sql, val)
  result = mycursor.fetchall()
  for photo in result:
    photo_list.append(photo["photo"])
  return photo_list

def load_attraction_data(result):
  attraction_data={}
  attraction_data["id"] = result["id"]
  attraction_data["name"] = result["name"]
  attraction_data["category"] = result["CAT"]
  attraction_data["description"] = result["description"]
  attraction_data["address"] = result["address"]
  attraction_data["transport"] = result["direction"]
  attraction_data["mrt"] = result["MRT"]
  attraction_data["lat"] = result["latitude"]
  attraction_data["lng"] = result["longitude"]
  id = result["id"]
  attraction_data["images"] = get_images (id)
  return attraction_data

def check_next_page_empty(page, keyword = None):
  if keyword is  None:
    mycursor = cnx1.cursor(dictionary = True)
    sql= "select * from taipei_attraction LIMIT %s, 12"
    val = ((page+1)*12,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return (len(result) == 0)
  if keyword is not None:
    mycursor = cnx1.cursor(dictionary = True)
    sql = "SELECT * FROM taipei_attraction WHERE MRT = %s or name like %s LIMIT %s , 12"
    val = (keyword, f"%{keyword}%" ,(page+1)*12)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return (len(result) == 0)
  
def get_attraction_by_keyword_page(keyword = None, page = 0):
    try:
      if keyword  is None: #無關鍵字
        response_joson ={}
        if check_next_page_empty(page): #下一頁有無
          response_joson["nextPage"] = None
        else:
          response_joson["nextPage"] = page+1
        response_data_list = []
        mycursor = cnx1.cursor(dictionary = True)
        sql= "select * from taipei_attraction LIMIT %s, 12"
        val = (page*12,)
        mycursor.execute(sql,val)
        data_list = mycursor.fetchall()
        for data in data_list:
          attraction_data = load_attraction_data(data)
          response_data_list.append(attraction_data)
        response_joson["data"] = response_data_list
        return response_joson
      elif keyword is not None: #有關鍵字
        response_joson ={}
        if check_next_page_empty(page, keyword): #下一頁有無
          response_joson["nextPage"] = None
        else:
          response_joson["nextPage"] = page+1
        response_data_list = []
        mycursor = cnx1.cursor(dictionary = True)
        sql= "select * from taipei_attraction WHERE MRT = %s OR name Like %s  LIMIT %s, 12 "
        val = (keyword, f"%{keyword}%", page*12)
        mycursor.execute(sql,val)
        data_list = mycursor.fetchall()
        for data in data_list:
          attraction_data = load_attraction_data(data)
          response_data_list.append(attraction_data)
        response_joson["data"] = response_data_list
        return response_joson
    except:
      print("錯誤")
      return None 