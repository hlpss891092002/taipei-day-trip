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

mycursor = cnx1.cursor()

def get_distinctMRT ():
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
  for MRT in MRT_List:
    count = M_C_dict[f"{MRT}"]
    sql = "INSERT INTO mrt_list(MRT_name, spot_count) values (%s, %s)"
    val = (f"{MRT}",count)
    print(f"{MRT}")
    print(count)
    mycursor.execute(sql, val)
    print(mycursor.rowcount, "record inserted in mrt_List.")
    cnx1.commit()
    
# MRT_List= get_distinctMRT()
# print(MRT_List)
# M_C_dict = get_MRT_spot_NUM(MRT_List)
# insert_MRT_count(MRT_List, M_C_dict)


def get_MRT_ORDERBY_spot_count():
  mrt_list = []
  sql = """SELECT MRT_name, spot_count FROM mrt_list ORDER BY spot_count DESC"""
  mycursor.execute(sql)
  result = mycursor.fetchall()
  for data in result:
    mrt = data[0]
    mrt_list.append(mrt)
  print(mrt_list)
  return(mrt_list)  

