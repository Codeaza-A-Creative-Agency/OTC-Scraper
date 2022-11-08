import requests
import pandas as pd
from savetodb import save_to_db
import mysql.connector
import smtplib
from smtplib import *
sender = 'faheem7450@gmail.com'
receivers = ['faheem7450@gmail.com']
host = '127.0.0.1'
mydb = mysql.connector.connect(
      host="localhost",
      user="faheem",
      password="1234",
      database= 'otc')
cur = mydb.cursor()
cur.execute("SELECT company_code FROM company")
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
def get_data(name):
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
        cur.execute(f"SELECT value FROM outstanding_shares where company_code='{name}' ORDER BY company_code DESC LIMIT 1")
        value= cur.fetchone()
        if value[0] != sharesValue:
            print(value[0])
            print(sharesValue)
            save_to_db(sharesValue,name,s_date)
            message = "Subject: Outstanding Shares value changed for " + name +"="+ str(sharesValue)
            return "Successfully added data to database"
            # try:
            #     smtpObj = smtplib.SMTP(host)
            #     smtpObj.sendmail(sender, receivers, message)         
            #     print("Successfully sent email")
            # except SMTPResponseException as e:
            #     error_code = e.smtp_code
            #     error_message = e.smtp_error
            #     print(error_code, error_message)
        else:
            return"No change found in outstanding shares"

    except:
        return "No data found for this company code :" + name
            
           
            
           
            



for name in names:
    # print(name[0])
    print(get_data(name[0]))