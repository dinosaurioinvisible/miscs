
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os

# 2020 - 2025  (up to 20/5/25)
# https://uk.finance.yahoo.com/quote/SQM-B.SN/history/?period1=1577836800&period2=1747785600    
# ticker = 'SQM-B.SN'
# start = 15778
# end = 17476          

os.chdir('../stock_data')
if os.path.isfile('divs.pkl'):
    dividends = pd.read_pickle('divs.pkl')
else:
    dividends = pd.DataFrame(columns=['Date','Dividend'])

def get_stock_data(ticker=None,start=15778,end=17476):
    url = f'https://uk.finance.yahoo.com/quote/{ticker}/history/?period1={start}36800&period2={end}99200'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    # get data
    response = requests.get(url, headers=headers)
    web = response.text
    soup = bs(web, 'html.parser')
    # data to df
    data = pd.DataFrame(columns=['Date', 'Open','High','Low','Close','AdjClose','Volume'])
    for day in soup.find('tbody').find_all('tr'):                   # for each day
        daydata = day.find_all('td')                                    # stock data
        if len(daydata) == 2:                                           # dividends are different (date,div)
            dividends.loc[len(dividends)] = [x.text.split()[0] for x in daydata]
        else:
            data.loc[len(data)] = [x.text for x in daydata]
    # save
    #data.to_csv(f'data_{ticker}_{start}_{end}.csv')
    #data.to_pickle(f'data_{ticker}_{start}_{end}.pkl')
    dividends.to_csv(f'divs_{start}_{end}.csv')
    dividends.to_pickle(f'divs_{start}_{end}.pkl')
    return data

if __name__ == '__main__':
    import sys
    print(f'\nticker: {sys.argv[1:][0]}\n')
    get_stock_data(sys.argv[1:][0])

