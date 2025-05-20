
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

ticker = 'SQM-B.SN'

end = 17476     # current (19/5/25)
start = 17000

url = f'https://uk.finance.yahoo.com/quote/{ticker}/history/?period1={start}16800&period2={end}99800'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)

web = response.text

web_data = bs(web, 'html.parser')

# with open(f'{ticker}_{start}_{end}_data', 'a') as f:
#   f.write(web_data)





