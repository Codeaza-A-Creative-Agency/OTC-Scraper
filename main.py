import requests
import pandas as pd
from savetodb import save_to_db
import mysql.connector
import smtplib
from smtplib import *
from email_sent import EmailSend

sender = 'faheem7450@gmail.com'
receivers = ['faheem7450@gmail.com']
email_obj = EmailSend()


host = '127.0.0.1'
mydb = mysql.connector.connect(
      host="localhost",
      user="app",
      password="1234",
      database= 'otc')
cur = mydb.cursor()
cur.execute("SELECT company_code FROM company where (status != 2 ) ")
names = cur.fetchall()
headers = {
    'authority': 'backend.otcmarkets.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,en-US;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://www.otcmarkets.com',
    'pragma': 'no-cache',
    'referer': 'https://www.otcmarkets.com/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

def update_status(name, status):
    cur.execute("update company set status = %s where company_code = %s", (status, name, ))
    mydb.commit()
def get_data(name):
    update_status(name, 2)
    params = {
    'symbol': name,
    }
    response = requests.get(f'https://backend.otcmarkets.com/otcapi/company/profile/full/{name}', params=params, headers=headers)
    try:
        resp= response.json()
        sharesValue=resp['securities'][0]['outstandingShares']
        share_date= resp['securities'][0]['outstandingSharesAsOfDate']
        s_date=pd.to_datetime(share_date, unit='ms').to_pydatetime()
        # save_to_db(sharesValue,name,s_date)
        cur.execute(f"SELECT value FROM outstanding_shares where company_code='{name}' ORDER BY id DESC LIMIT 1")
        value= cur.fetchone()
        if value is None or value[0] != sharesValue :
            
            # if company data already existed and now the shares have changed
            if(value is not None and value[0] != sharesValue):
                previous_shares = "{:,}".format(int(value[0]))
                new_shares = "{:,}".format(int(sharesValue))
                if (sharesValue > value[0]):
                    shares_change = "increased"
                else:
                    shares_change = "decreased"
                change_percentage = round(((sharesValue - value[0])/value[0])*100,2)
                change_value = "{:,}".format(int(sharesValue - value[0]))
                email_obj.send_email("OTC Markets Shares Changed", f"Shares for {name} have been {shares_change} by {change_value} ({change_percentage}%) from {previous_shares} to {new_shares}")

            save_to_db(sharesValue,name,s_date)
            update_status(name , 3)
            return "Successfully added data to database"
            
        else:
            update_status(name, 3)
            return"No change found in outstanding shares"

    except Exception as e:
        if ("securities" in str(e)):
            update_status(name, 5)
            return "Temporary Error"
        update_status(name, 4)
        return "No data found for this company code :" + name + " error: "+str(e)
            
           
            
           
            



for name in names:
    # print(name[0])
    print(get_data(name[0]))