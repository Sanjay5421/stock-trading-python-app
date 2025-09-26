import requests
import os
import time
import csv

from dotenv import load_dotenv
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit=1000&sort=ticker&apiKey={POLYGON_API_KEY}'
response = requests.get(url)

tickers = []

data = response.json()
for ticker in data['results']:
    tickers.append(ticker)


while 'next_url' in data:
    print('Requesting next page', data['next_url'])
    response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
    data = response.json()
    print(data)
    for ticker in data['results']:
        tickers.append(ticker)
    time.sleep(12)

example_ticker = {'ticker': 'ZVIA', 
    'name': 'Zevia PBC', 
    'market': 'stocks', 
    'locale': 'us', 
    'primary_exchange': 'XNYS', 
    'type': 'CS', 
    'active': True, 
    'currency_name': 'usd', 
    'cik': '0001854139', 
    'composite_figi':
    'BBG011S2NX76', 
    'share_class_figi': 'BBG011S2NY29', 
    'last_updated_utc': '2025-09-26T06:06:19.270877283Z'}

fieldnames = list(example_ticker.keys())
output_csv = 'tickers.csv'
with open(output_csv, mode = 'w', newline = '', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for t in tickers:
        row = {key: t.get(key, '') for key in fieldnames}
        writer.writerow(row)

print(f'Wrote {len(tickers)} rows to {output_csv}')    
