
import mysql.connector
import mysql.connector.pooling
from dotenv import load_dotenv
import os
load_dotenv()

def connection():
  try:
    dbconfig = {
        "host": os.getenv("DBHOST"),
        "user": os.getenv("DBUSER"),
        "password": os.getenv("DBPASSWORD"),
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
    print("db connection fail in db_create_member_page")

def create_booking_table():
  con = connection()
  cursor = con.cursor(dictionary = True)
  try:
    sql= """
    CREATE TABLE booking_order_table(
     id BIGINT AUTO_INCREMENT,
    member_id BIGINT NOT NULL,
    attraction_id BIGINT NOT NULL,
    date  datetime NOT NULL,
    time varchar(255) NOT NULL,
    price int not null,
    order_time datetime NOT NULL DEFAULT(CURRENT_TIME()),
     primary key(id),
     foreign key (member_id) references member_table(id),
     foreign key (attraction_id) references taipei_attraction(id)
     );
    """
    cursor.execute(sql,)
    print("create  booking_order_table")
  except:
    print(" create booking table fail")
  finally:
    cursor.close()
    con.close()

create_booking_table()