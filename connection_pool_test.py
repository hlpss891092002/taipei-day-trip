import mysql.connector
import mysql.connector.pooling
import json

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

mycursor = cnx1.cursor()
