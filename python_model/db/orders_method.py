from python_model.db.db_connection import *
from datetime import *

def insert_order_table(member_id, contact, order):
  now = datetime.now().strftime('%Y%m%d')
  con = connection()
  cursor = con.cursor(dictionary = True)
  attraction_id = order.trip.attraction.id
  date = order.date
  time = order.time
  price = order.price
  pay_state = "UNPAID"
  order_id = str(now)+"-"+str(member_id)+"-"+str(attraction_id)+str(date)+time[0].upper()
  contact_name = contact.name
  contact_email = contact.email
  contact_phone = contact.phone

  formatted_date = date.strftime('%Y-%m-%d')
  try:
    sql = """REPLACE INTO orders_table (id, member_id, attraction_id, date, time, price, contact_name, contact_email, contact_phone, pay_state)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    val = (order_id, member_id, attraction_id ,formatted_date, time, price,contact_name, contact_email, contact_phone, pay_state)
    cursor.execute(sql, val)
    con.commit()
    print("insert one order")
    return order_id
  except Exception as e:
    print(f"fail to insert one order on {e}")
    return False
  finally:
    cursor.close()
    con.close()

def turn_to_paid(order_id):
  con = connection()
  cursor = con.cursor(dictionary = True)
  try:
    sql = """UPDATE orders_table 
     SET pay_state = %s
     WHERE  id = %s
    """
    val = ("PAID", order_id)
    cursor.execute(sql, val)
    con.commit()
    print(f"id : {order_id} pay_state update to PAID")
    return order_id
  except Exception as e:
    print(f"id : {order_id} pay_state update fail")
    return False
  finally:
    cursor.close()
    con.close()

def getOrderData(order_id):
  con = connection()
  cursor = con.cursor(dictionary = True)
  try:
    sql = """SELECT orders_table.id as number, price, contact_name, contact_email, contact_phone, date, time, pay_state as status, photo as image, attraction_data.id AS attraction_id, name, address  FROM (SELECT taipei_attraction.id as id, name, address, photo FROM taipei_attraction 
    INNER JOIN photo_file ON 
    taipei_attraction.id = photo_file.attraction_id ) as attraction_data INNER JOIN orders_table ON attraction_data.id = orders_table.attraction_id
    where orders_table.id = %s
    LIMIT 1
    """

    val = (order_id,)
    cursor.execute(sql, val)
    raw_data = cursor.fetchone()
    orderData = {}
    data = {}
    contact = {}
    trip = {}
    attraction = {}
    number, price, contact_name, contact_email, contact_phone, date, time, status, image, attraction_id, name, address, *rest = raw_data.values()
    attraction["id"] = attraction_id
    attraction["name"] = name
    attraction["address"] = address
    attraction["image"] = image
    trip["attraction"] = attraction
    trip["date"] = date.strftime('%Y-%m-%d')
    trip["time"] = time
    contact["name"] = contact_name
    contact["email"] = contact_email
    contact["phone"] = contact_phone
    data["number"] = number
    data["price"] = price

    data["trip"] = trip

    data["contact"] = contact
    if status == "PAID":
      data["status"] = 1
    else:
      data["status"] = 0
    orderData["data"] = data
    return orderData
  
  # except Exception as e:
  #   print(f"get order fail on {e}")
    return 
  finally:
    cursor.close()
    con.close()