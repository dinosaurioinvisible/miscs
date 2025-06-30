
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os
import pickle


class Stock():
    def __init__(self,ticker,name=None,data=None,url=None,start=15778,end=17476):
        self.ticker = ticker
        self.name = name if name else ticker
        self.data = data if data else pd.DataFrame(columns=['Date', 'Open','High','Low','Close','AdjClose','Volume','Div'])
        self.start = start
        self.end = end
        self.min_start = start
        self.max_end = end
        self.url = self.update_url(url)

    # TODO: load previous pickle
    def load_data():
        pass

    def update_url(self,url=None,start=0,end=0):
        if url:
            # this should allow new start and end
            self.url = url
        else:
            # to keep track of start/end for saving
            if start > 0:
                self.min_start = start if start < self.min_start else self.min_start
                self.start = start
            if end > start:
                self.max_end = end if end > self.max_end else self.max_end
                self.end = end
            self.url = f'https://uk.finance.yahoo.com/quote/{self.ticker}/history/?period1={self.start}36800&period2={self.end}99200'

    def reset_start_end(self):
        self.start = self.min_start
        self.end = self.max_end

    def get_data(self,start=0,end=0):
        if start > 0 and end > start:
            self.update_url(start=start,end=end)
        # get raw text from site
        text = self.mk_stock_request()
        # clean data and formar in pd
        data = self.mk_stock_data(text)
        
    # to get text from a website
    def mk_stock_request(self,headers=None):
        if not headers:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        response = requests.get(self.url, headers=headers)
        return response.text
    
    # parse stock data from text
    def mk_stock_data(self,text):
        soup = bs(text, 'html.parser')
        data = pd.DataFrame(columns=['Date', 'Open','High','Low','Close','AdjClose','Volume','Div'])
        for day in soup.find('tbody').find_all('tr'):                       # for each day
            daydata = day.find_all('td')                                    # stock data
            if len(daydata) == 2:                                           # dividends are different (date,div)
                date, div = [x.text.split() for x in daydata]
                data.loc[len(self.data)] = [date] + [0,0,0,0,0,0] + [div]
            elif len(daydata) > 2:
                data.loc[len(self.data)] = [x.text for x in daydata] + [0]
            else:
                print(f'\nunknown format: {daydata}')
        return data
    
    # TODO
    def update_stock_data(self):
        pass
    
    def to_pkl(self):
        self.data.to_pickle(f'data_{self.ticker}_{start}_{end}.pkl')
    def to_csv(self):
        self.data.to_csv(f'data_{self.ticker}_{start}_{end}.csv')