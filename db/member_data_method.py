from db.db_connection import *


def add_member(name, email, password):
  con = connection()
  cursor = con.cursor(dictionary = True)
  try:
    sql_search ="""SELECT email from member_table WHERE email = %s"""
    val_search = (email,)
    cursor.execute(sql_search,val_search)
    result = cursor.fetchone()
    if result == None :
      sql_add ="""INSERT INTO member_table(name, email, password)
      VALUES(%s, %s, %s)
      """
      val_add = (name, email, password)
      cursor.execute(sql_add, val_add)
      con.commit()
      print("add one member")
      return True
    else:
      return "電子郵件重複註冊，請更換電子郵件"
  except:
    print("fail to add member")
  finally:
    cursor.close()
    con.close()

def signin(email, password):
  con = connection()
  cursor = con.cursor(dictionary = True)
  try: 
    sql ="""SELECT * from member_table WHERE email = %s and password = %s"""
    val = (email, password)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    return result
  except:
    print("member is not exist")
  finally:
    con.close()
    cursor.close()

def check_member(id, email):
  con = connection()
  cursor = con.cursor(dictionary = True)
  try: 
    sql ="""SELECT * from member_table WHERE id = %s and email = %s"""
    val = (id, email)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    return result
  except:
    print("fail to add member")
  finally:
    con.close()
    cursor.close()