import mysql.connector
import mysql.connector.pooling
import json
import logging

logging_FORMAT = '%(asctime)s %(levelname)s : %(message)s %(funcName)s  %(lineo)d '
logging.basicConfig(filename="db_searchlogging", level=logging.DEBUG, format=logging_FORMAT)

def connection():
  try:
    dbconfig = {
        "host":"0.0.0.0",
        "user":"lucas",
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
    logging.warning("database connection fail")


def check_next_page_empty(keyword = None, page = 0):
  try:
    cnx1 = connection()
    if keyword is  None:
      mycursor = cnx1.cursor(dictionary = True)
      sql= "select id from taipei_attraction LIMIT %s, 13"
      val = ((page)*12,)
      mycursor.execute(sql, val)
      result = mycursor.fetchall()
      if len(result) > 12:
        return  page + 1
      else:
        return None
    if keyword is not None:
      mycursor = cnx1.cursor(dictionary = True)
      sql = "SELECT * FROM taipei_attraction WHERE MRT = %s or name like %s LIMIT %s , 13"
      val = (keyword, f"%{keyword}%" ,(page)*12)
      mycursor.execute(sql, val)
      result = mycursor.fetchall()
      if len(result) > 12:
        return  page + 1
      else:
        return None
  except:
    logging.warning("error in empty def")
  finally:
    mycursor.close()
    cnx1.close()



def get_attraction_by_keyword_page(keyword = None, page = 0):
    try:
      cnx1 = connection()
      if keyword  is None: #無關鍵字
        mycursor = cnx1.cursor(dictionary = True)
        sql= """
        SELECT taipei_attraction.id, name, CAT as category, description, address, direction as transport, mrt, ROUND(latitude) as lat, ROUND(longitude) as lng, group_concat(photo) as images  FROM taipei_attraction 
        JOIN photo_file 
        ON  photo_file.attraction_id = taipei_attraction.id
        group by taipei_attraction.id  limit %s, 12
        """
        val = (page*12,)
        mycursor.execute(sql,val)
        attraction_data_list = mycursor.fetchall()
        for attraction in attraction_data_list:
          attraction["images"] = attraction["images"].split(",")
        return attraction_data_list

      elif keyword is not None: #有關鍵字
        response_data_list = []
        mycursor = cnx1.cursor(dictionary = True)
        sql= """ SELECT taipei_attraction.id, name, CAT as category, description, address, direction as transport, mrt, ROUND(latitude) as lat, ROUND(longitude) as lng, group_concat(photo) as images  
        FROM taipei_attraction 
        JOIN photo_file 
        ON  photo_file.attraction_id = taipei_attraction.id
        WHERE MRT = %s OR name Like %s
        group by taipei_attraction.id 
        LIMIT %s, 12 """
        val = (keyword, f"%{keyword}%", page*12)
        mycursor.execute(sql,val)
        attraction_data_list = mycursor.fetchall()
        for attraction in attraction_data_list:
          attraction["images"] = attraction["images"].split(",")
        return attraction_data_list
    except:
      print("錯誤")
      logging.warning("error in def get_attraction_by_keyword_pag")
      return None 
    finally:
      mycursor.close()
      cnx1.close()

    
def get_attraction_by_id(id):
  try:
    cnx1 = connection()
    # attraction_data={}
    mycursor = cnx1.cursor(dictionary = True)
    sql1= """SELECT id, name, CAT as category, description, address, direction as transport, mrt, ROUND(latitude) as lat, ROUND(longitude) as lng  FROM taipei_attraction  WHERE id = %s"""
    sql_photo = """SELECT photo FROM photo_file 
    WHERE attraction_id = %s"""
    val = (f"{id}",)
    mycursor.execute(sql1, val)
    result = mycursor.fetchone()
    mycursor.execute(sql_photo, val)
    image_list = mycursor.fetchall()
    print(image_list)
    result["images"] = []
    for image in image_list:
      result["images"].append(image["photo"])
    return result
    
    
  except:
    logging.log("error in get_attraction_by_keyword_page")
    return None
  finally:
    mycursor.close()
    cnx1.close() 

def get_MRT_ORDERBY_spot_count():
  try:
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
  except:
    logging.info("error in def MRT orderby")
