import logging
from model.db_connection import *
from dotenv import load_dotenv

load_dotenv()

logging_FORMAT = '%(asctime)s %(levelname)s : %(message)s %(funcName)s  %(lineo)d '
logging.basicConfig(filename="db_searchlogg.log", level=logging.DEBUG, format=logging_FORMAT)


def get_attraction_by_keyword_page(keyword = None, page = 0):
    cnx1 = connection()
    mycursor = cnx1.cursor(dictionary = True)
    response_data = {}
    try:
      if keyword  is None: #無關鍵字
        sql= """
        SELECT taipei_attraction.id, name, CAT as category, description, address, direction as transport, mrt, ROUND(latitude) as lat, ROUND(longitude) as lng, group_concat(photo) as images  FROM taipei_attraction 
        JOIN photo_file 
        ON  photo_file.attraction_id = taipei_attraction.id
        group by taipei_attraction.id  limit %s, 13
        """
        val = (page*12,)
        mycursor.execute(sql,val)
        attraction_data_list = mycursor.fetchall()
        for attraction in attraction_data_list:
          attraction["images"] = attraction["images"].split(",")
        if(len(attraction_data_list) == 13):
          del attraction_data_list[12]
          response_data["nextPage"] = page+1
          response_data["data"] = attraction_data_list
        else:
          response_data["nextPage"] = None
          response_data["data"] = attraction_data_list
        return response_data
      elif keyword is not None: #有關鍵字
        sql= """ SELECT taipei_attraction.id, name, CAT as category, description, address, direction as transport, mrt, ROUND(latitude) as lat, ROUND(longitude) as lng, group_concat(photo) as images  
        FROM taipei_attraction 
        JOIN photo_file 
        ON  photo_file.attraction_id = taipei_attraction.id
        WHERE MRT = %s OR name Like %s
        group by taipei_attraction.id 
        LIMIT %s, 13 """
        val = (keyword, f"%{keyword}%", page*12)
        mycursor.execute(sql,val)
        attraction_data_list = mycursor.fetchall()
        for attraction in attraction_data_list:
          attraction["images"] = attraction["images"].split(",")
        if(len(attraction_data_list) == 13):
          del attraction_data_list[12]
          response_data["nextPage"] = page+1
          response_data["data"] = attraction_data_list
        else:
          response_data["nextPage"] = None
          response_data["data"] = attraction_data_list
        return response_data
    except:
      print("錯誤")
      logging.warning("error in def get_attraction_by_keyword_pag")
      return None 
    finally:
      mycursor.close()
      cnx1.close()
 
def get_attraction_by_id(id):
  cnx1 = connection()
  mycursor = cnx1.cursor(dictionary = True)
  try:
    sql1= """SELECT id, name, CAT as category, description, address, direction as transport, mrt, ROUND(latitude) as lat, ROUND(longitude) as lng  FROM taipei_attraction  WHERE id = %s"""
    sql_photo = """SELECT photo FROM photo_file 
    WHERE attraction_id = %s"""
    val = (f"{id}",)
    mycursor.execute(sql1, val)
    result = mycursor.fetchone()
    mycursor.execute(sql_photo, val)
    image_list = mycursor.fetchall()
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
  cnx1 = connection()
  mycursor = cnx1.cursor()
  try:
    mrt_list = []
    sql = """SELECT MRT 
            FROM taipei_attraction
            WHERE MRT IS NOT NULL
            GROUP BY MRT
            ORDER BY count(*) DESC"""
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for data in result:
      mrt = data[0]
      if mrt != "None":
        mrt_list.append(mrt)
    return mrt_list
  except:
    logging.info("error in def MRT orderby")
  finally:
    mycursor.close()
    cnx1.close() 
