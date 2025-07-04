
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os

# 2020 - 2025  (up to 20/5/25)
# https://uk.finance.yahoo.com/quote/SQM-B.SN/history/?period1=1577836800&period2=1747785600    
# ticker = 'SQM-B.SN'
# start = 15778
# end = 17476

# specify dir
os.chdir('../stock_data')
if os.path.isfile('divs.pkl'):
    dividends = pd.read_pickle('divs.pkl')
else:
    dividends = pd.DataFrame(columns=['Company','Date','Dividend'])

# to get text from a website
def mk_stock_request(url,headers=0):
    if headers==0:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response.text

# parse stock data from text
def add_stock_data(text):
    soup = bs(text, 'html.parser')
    data = pd.DataFrame(columns=['Date', 'Open','High','Low','Close','AdjClose','Volume','Div'])
    for day in soup.find('tbody').find_all('tr'):                       # for each day
        daydata = day.find_all('td')                                    # stock data
        if len(daydata) == 2:                                           # dividends are different (date,div)
            data.loc[len(dividends)] = [ticker]+[x.text.split()[0] for x in daydata] 
        elif len(daydata) > 2:
            data.loc[len(data)] = [x.text for x in daydata]
        else:
            print(f'\nunknown format: {daydata}')
    return data

# parse dividends data from text
def add_div_data(text,ticker):
    soup = bs(text, 'html.parser')
    div_data = pd.DataFrame(columns=['Date',])
    for day in soup.find('tbody').find_all('tr'):
        daydata = day.find_all('td')
        if len(daydata) == 2:                                           # dividends are different (date,div)
            div_data.loc[len(dividends)] = [ticker]+[x.text.split()[0] for x in daydata]
    return div_data

# name of ipsa corps
def get_ipsa_stocks(url_ipsa='https://uk.finance.yahoo.com/quote/%5EIPSA/components/',
                    start=15778,
                    end=17476):
    ipsa_dict = {}
    text = mk_stock_request(url_ipsa)
    soup = bs(text, 'html.parser')
    for tr in soup.find('tbody').find_all('tr'):
        ticker = tr.find('a').text
        name = tr.find_all('span')[1].text
        url = f'https://uk.finance.yahoo.com/quote/{ticker}/history/?period1={start}36800&period2={end}99200'
        ipsa_dict[ticker] = [ticker, name, url]
    return ipsa_dict


class Stock():
    def __init__(self,ticker,name=None,url=None,data=None,start=15778,end=17476):
        self.ticker = ticker
        self.name = name if name else ticker
        self.url = url
        self.data = data

    def get_data(self,start=0,end=0):
        start = start if start > 0 else self.start
        end = end if end > abs(start) else self.end
        text = mk_stock_request(self.url)
        self.data = add_stock_data(text,self.ticker)
        self.div_data = add_div_data(text,self.ticker)
    
    def to_pkl(self):
        self.data.to_pickle(f'data_{self.ticker}_{start}_{end}.pkl')
        dividends.to_pickle(f'divs_{start}_{end}.pkl')
    def to_csv(self):
        self.data.to_csv(f'data_{self.ticker}_{start}_{end}.csv')
        self.dividends.to_csv(f'divs_{start}_{end}.csv')
    

# the idea is to compare EFTs
# class ETF(Stock):
#     def __init__(self,ticker,name=None):
#         super().__init__(ticker,name)
#         self.comps = []



def get_stocks_data(tickers,start=0,end=0):
    start, end = int(start), int(end)
    for ticker in tickers:
        mk_ticker = True
        for filename in os.listdir():
            if filename.split('.')[-1] == 'pkl':
                if filename.split('_')[1] == ticker:
                    file_start = int(filename.split('_')[2])
                    file_end = int(filename.split('_')[3].split('.')[0])
                    if start > 0 and start < file_start:
                        if end > start and end > file_end:
                            pass
                        else:
                            end = file_start
                    elif end > file_end:
                        start = file_end
                    else:
                        mk_ticker = False
                        print(f'\n{ticker} already done\n')
        if mk_ticker:
            print(f'\ngetting {ticker} data\n')
            if start > 0 and end > start:
                get_data(ticker, start, end)
            else:
                get_data(ticker)
            print(f'done\n')

def get_data(ticker,start=15778,end=17476,to_csv=False,to_pkl=False):
    url = f'https://uk.finance.yahoo.com/quote/{ticker}/history/?period1={start}36800&period2={end}99200'
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    # get data
    # response = requests.get(url, headers=headers)
    # web = response.text
    text = mk_stock_request(url)
    soup = bs(text, 'html.parser')
    # data to df
    data = pd.DataFrame(columns=['Date', 'Open','High','Low','Close','AdjClose','Volume'])
    for day in soup.find('tbody').find_all('tr'):                       # for each day
        daydata = day.find_all('td')                                    # stock data
        if len(daydata) == 2:                                           # dividends are different (date,div)
            dividends.loc[len(dividends)] = [ticker]+[x.text.split()[0] for x in daydata]
        else:
            data.loc[len(data)] = [x.text for x in daydata]
    # save
    # if to_csv:
    #     data.to_csv(f'data_{ticker}_{start}_{end}.csv')
    #     dividends.to_csv(f'divs_{start}_{end}.csv')
    # if to_pkl:
    #     data.to_pickle(f'data_{ticker}_{start}_{end}.pkl')
    #     dividends.to_pickle(f'divs_{start}_{end}.pkl')
    return data

if __name__ == '__main__':
    import sys
    tickers = []
    start, end = 0, 0
    arguments = sys.argv[1:]
    for ei in range(len(arguments)):
        if arguments[ei] == '--start':
            tickers = arguments[:ei]
            start = arguments[ei+1]
        if arguments[ei] == '--end':
            end = arguments[ei+1]
            if start == 0:
                tickers = arguments[:ei]
    if tickers == 'all' or tickers == []:
        tickers = ['BCH', 'SQM-B.SN', 'CENCOSUD.SN', 'BSAC', 'FALABELLA.SN', 'LTM','COPEC.SN', 'ENELAM.SN', 'CMPC.SN','VAPORES.SN']
    print(f'\ntickers: {tickers}\nstart={start}, end={end}\n')
    get_stocks_data(tickers,start,end)