import requests
import json
import pandas as pd
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

params = {
    'symbol': 'CPMD',
}

response = requests.get('https://backend.otcmarkets.com/otcapi/company/profile/full/CPMD', params=params, headers=headers)
resp= response.json()
def get_data():
    sharesValue=resp['securities'][0]['outstandingShares']
    share_date= resp['securities'][0]['outstandingSharesAsOfDate']
    s_date=pd.to_datetime(share_date, unit='ms').to_pydatetime()
   
    return sharesValue,s_date


print(get_data())