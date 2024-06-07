import mysql.connector
import mysql.connector.pooling
import json
import logging

logging_FORMAT = '%(asctime)s %(levelname)s : %(message)s %(funcName)s  %(lineo)d '
logging.basicConfig(filename="db_searchlogging", level=logging.DEBUG, format=logging_FORMAT)

def connection():
  try:
    dbconfig = {
        "host":"localhost",
        "user":"root",
        "password":"00000000",
        "database":"wehelp_stage2_taipei_spot",
    }
    cnxpool = mysql.connector.pooling.MySQLConnectionPool(
      pool_name="mypool",
      pool_size=3,
      **dbconfig
    )
    cnx1 = cnxpool.get_connection()
    return cnx1
  except:
    logging.info("database connection fail")




def get_images (id):
  try:
    cnx1 = connection()
    mycursor =cnx1.cursor(dictionary = True)
    photo_list = []
    sql = "select photo from photo_file where attraction_id = %s"
    val = (id, )
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    for photo in result:
      photo_list.append(photo["photo"])
    return photo_list
  except:
    print("error in get image def")
  finally:
    mycursor.close()
    cnx1.close()


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
  try:
    cnx1 = connection()
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
  except:
    print("error in empty def")
  finally:
    mycursor.close()
    cnx1.close()



def get_attraction_by_keyword_page(keyword = None, page = 0):
    try:
      cnx1 = connection()
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
    finally:
      mycursor.close()
      cnx1.close()

    
def get_attraction_by_id(id):
  try:
    cnx1 = connection()
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
    photo_list = get_images (id)
    attraction_data["images"] = photo_list
    return (attraction_data)
  except:
    return None
  finally:
    mycursor.close()
    cnx1.close() 

def get_MRT_ORDERBY_spot_count():
  cnx1 = connection()
  mycursor = cnx1.cursor()
  mrt_list = []
  sql = """SELECT MRT 
          FROM taipei_attraction
          WHERE MRT IS NOT NULL
          GROUP BY MRT
          ORDER BY count(*) DESC"""
  mycursor.execute(sql)
  result = mycursor.fetchall()
  mycursor.close()
  cnx1.close()  
  for data in result:
    mrt = data[0]
    if mrt != "None":
      mrt_list.append(mrt)
  return mrt_list
 
get_MRT_ORDERBY_spot_count()
