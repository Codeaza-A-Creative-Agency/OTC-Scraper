import requests
import json
import pandas as pd
from savetodb import save_to_db
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


names = ['ZURVY', "AMZN", "CPMD","SIHBY","MVPT","GBTC","ADYEY"]
ids=1
for name in names:
    params = {
    'symbol': name,
    }
    response = requests.get(f'https://backend.otcmarkets.com/otcapi/company/profile/full/{name}', params=params, headers=headers)
    print(response.url)
    resp= response.json()
    sharesValue=resp['securities'][0]['outstandingShares']
    share_date= resp['securities'][0]['outstandingSharesAsOfDate']
    s_date=pd.to_datetime(share_date, unit='ms').to_pydatetime()
    print(sharesValue, s_date)
    save_to_db(ids,sharesValue,name,s_date)
    ids +=1