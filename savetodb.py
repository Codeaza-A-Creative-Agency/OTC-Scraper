import mysql.connector
def save_to_db(id_,value,c_code,date):
    print("Hello world")
    mydb = mysql.connector.connect(
      host="localhost",
      user="faheem",
      password="1234",
      database= 'otc')
    cur = mydb.cursor()
    sql = "INSERT INTO outstanding_shares (id, value,company_code,date_created) values (%s,%s,%s,%s)"
    val= (id_,value,c_code,date)
    cur.execute(sql,val)
    mydb.commit()
    
    return str(cur.rowcount) + "record inserted"
    