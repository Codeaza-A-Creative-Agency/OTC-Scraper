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
cur.execute("SELECT value FROM outstanding_shares")
values= cur.fetchall()
def get_data(name):
    params = {
    'symbol': name,
    }
    response = requests.get(f'https://backend.otcmarkets.com/otcapi/company/profile/full/{name}', params=params, headers=headers)
    resp= response.json()
    sharesValue=resp['securities'][0]['outstandingShares']
    share_date= resp['securities'][0]['outstandingSharesAsOfDate']
    s_date=pd.to_datetime(share_date, unit='ms').to_pydatetime()
    # save_to_db(sharesValue,name,s_date)
    for i in values:
        if i[0] != sharesValue:
            save_to_db(sharesValue,name,s_date)
            message = "Subject: Outstanding Shares value changed for " + name +"="+ str(sharesValue)
            try:
                smtpObj = smtplib.SMTP(host)
                smtpObj.sendmail(sender, receivers, message)         
                print("Successfully sent email")
            except SMTPResponseException as e:
                error_code = e.smtp_code
                error_message = e.smtp_error
                print(error_code, error_message)
        else:
            print("No change in outstanding shares")
            
           
            
           
    return "Done"
            



for name in names:
    # print(name[0])
    get_data(name[0])