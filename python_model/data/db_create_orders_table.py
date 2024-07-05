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
  except  Exception as e:
    print(f"Error inserting new booking: {e}")

def create_orders_table():
  con = connection()
  cursor = con.cursor(dictionary = True)
  try:
    sql = """
    CREATE TABLE orders_table(
    id varchar(255),    
    member_id BIGINT NOT NULL,
    attraction_id BIGINT NOT NULL,
    date  datetime NOT NULL,
    time varchar(255) NOT NULL,
    price int not null,
    order_time datetime NOT NULL DEFAULT(CURRENT_TIME()),
    primary key(id),
    contact_name varchar(255) null,
    contact_email varchar(255) null,
    contact_phone varchar(255) null,
     pay_state varchar(255) null,
    foreign key (member_id) references member_table(id),
    foreign key (attraction_id) references taipei_attraction(id)
    );
    """
    cursor.execute(sql,)
    print("create table orders_table")
  except Exception as e:
    print(f"create table member_table fail on {e}")
  finally:
    cursor.close()
    con.close()



create_orders_table()