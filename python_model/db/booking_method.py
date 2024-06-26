from python_model.db.db_connection import *
from datetime import *

def insert_booking_order(member_id, attractionId, date, time, price):
  con = connection()
  cursor = con.cursor(dictionary = True)
  formatted_date = date.strftime('%Y-%m-%d')
  try:
    sql_get_order_id = """select id  FROM booking_order_table where member_id = %s """
    val_get_order_id = (member_id, )
    cursor.execute(sql_get_order_id, val_get_order_id)
    result = cursor.fetchone()
    print(result)
    if (result is None):  
      order_id = result
    else:
      order_id = result["id"] 
    print(order_id)
    sql = """REPLACE INTO booking_order_table (id, member_id, attraction_id, date, time, price)
    VALUES(%s, %s, %s, %s, %s, %s)
    """
    val = (order_id, member_id, attractionId ,formatted_date, time, price)
    cursor.execute(sql, val)
    con.commit()
    print("insert one order")
    return True
  except:
    print("fail to insert one order")
    return False
  finally:
    cursor.close()
    con.close()

def render_booking_order(member_id):
  con = connection()
  cursor = con.cursor(dictionary = True, buffered=True)
  try:
    sql_order = """SELECT attraction_id as attraction, date, time, price FROM booking_order_table WHERE member_id = %s
    """
    val_order = (member_id,)
    cursor.execute(sql_order, val_order)
    booking = cursor.fetchone()
    booking["date"] = booking["date"].strftime('%Y-%m-%d')
    sql_attraction = """SELECT taipei_attraction.id, name, address, photo as image
    FROM   taipei_attraction JOIN photo_file 
        ON  photo_file.attraction_id = taipei_attraction.id WHERE taipei_attraction.id = %s
    """
    val_attraction = (booking["attraction"],)
    cursor.execute(sql_attraction, val_attraction)
    attraction = cursor.fetchone()
    print(attraction)
    booking["attraction"] = attraction
    print("get booking order ")
    return booking  
  except:
    print("fail to get booking order ")
  finally:
    cursor.close()
    con.close()

def delete_booking(member_id):
  con = connection()
  cursor = con.cursor(dictionary = True)
  formatted_date = date.strftime('%Y-%m-%d')
  try:
   pass
  except:
    print("fail to get booking order ")
  finally:
    cursor.close()
    con.close()