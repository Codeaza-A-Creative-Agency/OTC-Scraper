import mysql.connector
def save_to_db(value,c_code,date):
    mydb = mysql.connector.connect(
      host="localhost",
      user="faheem",
      password="1234",
      database= 'otc')
    cur = mydb.cursor()
    sql = "INSERT INTO outstanding_shares (value,company_code,date_created) values (%s,%s,%s)"
    val= (value,c_code,date)
    cur.execute(sql,val)
    mydb.commit()
    
    return str(cur.rowcount) + "record inserted"
    