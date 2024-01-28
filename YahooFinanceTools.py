import pandas as pd
import pandas_ta as ta
import numpy as np
import yfinance as yf
import os
from pandas_datareader import data as pdr
from datetime import datetime



yf.pdr_override()

class StockUtils:
    def __init__(self, ticker, date_start, date_end, file_path, file_name, time_interval):
        self.ticker = ticker
        self.date_start = date_start
        self.date_end = date_end
        self.file_path = file_path
        self.file_name = file_name
        self.time_interval = time_interval
        self.data_file_path = os.path.join(self.file_path, self.file_name)
    
    def DataToCSV(self):
        stock_Data = pdr.get_data_yahoo(f'{self.ticker}', start=self.date_start, end=self.date_end, interval=self.time_interval)
        stock_Data['EMA20'] = ta.ema(stock_Data['Close'], length=20)
        stock_Data['EMA26'] = ta.ema(stock_Data['Close'], length=26)
        stock_Data['EMA50'] = ta.ema(stock_Data['Close'], length=50)
        stock_Data['DEMA20'] = ta.dema(stock_Data['Close'], length=20)
        stock_Data['DEMA26'] = ta.dema(stock_Data['Close'], length=26)
        stock_Data['DEMA50'] = ta.dema(stock_Data['Close'], length=50)
        stock_Data['MACD'] = ta.macd(stock_Data['Close'], fast=12, slow=26, signal=9)['MACD_12_26_9']
        stock_Data['MACD-HISTOGRAM'] = ta.macd(stock_Data['Close'], fast=12, slow=26, signal=9)['MACDh_12_26_9']
        stock_Data['MACD-SIGNAL'] = ta.macd(stock_Data['Close'], fast=12, slow=26, signal=9)['MACDs_12_26_9']
        stock_Data['RSI5'] = ta.rsi(stock_Data['Close'], length=5)
        stock_Data['RSI14'] = ta.rsi(stock_Data['Close'], length=14)
        stock_Data['RSI21'] = ta.rsi(stock_Data['Close'], length=21)
        stock_Data['RSI5SIGNAL'] = 50
        stock_Data.loc[stock_Data['RSI5'] > 80, 'RSI5SIGNAL'] = 100
        stock_Data.loc[stock_Data['RSI5'] < 20, 'RSI5SIGNAL'] = 0
        stock_Data['RSI14SIGNAL'] = 50
        stock_Data.loc[stock_Data['RSI14'] > 80, 'RSI14SIGNAL'] = 100
        stock_Data.loc[stock_Data['RSI14'] < 20, 'RSI14SIGNAL'] = 0
        stock_Data['RSI21SIGNAL'] = 50
        stock_Data.loc[stock_Data['RSI21'] > 80, 'RSI21SIGNAL'] = 100
        stock_Data.loc[stock_Data['RSI21'] < 20, 'RSI21SIGNAL'] = 0
        stock_Data.to_csv(self.data_file_path, header=True)


        
def RegionSelector():
        region = input('[1] US STOCK\n[2] AUS STOCK\n-> ')
        print('')
        if region == '2':
            region = '.AX'
        else:
            region = ''
        return region



def SingleStockRawData(folder_path, ticker, date_from, region, time_interval):
    stock_data = StockUtils(f'{ticker}{region}', date_from, datetime.date(datetime.now()), folder_path, f'{ticker}.csv', time_interval)
    stock_data.DataToCSV()

def StockListRawData(stock_list_file_path, folder_path, date_from, region, time_interval):
    stock_list_file = open(stock_list_file_path)
    stock_list = stock_list_file.read()
    stock_list = stock_list.replace('\n', '.').split('.')
    for ticker in stock_list:
        stock_data = StockUtils(f'{ticker}{region}', date_from, datetime.date(datetime.now()), folder_path, f'{ticker}.csv', time_interval)
        stock_data.DataToCSV()
    stock_list_file.close()



def ToolSelector():
    options = input('[1] Fetch Data for 1 Stock\n[2] Fetch Data for List of Stocks\n-> ')
    print('')

    if options == '1':
        folder_path = input('Destination Folder Path: ')
        ticker = input('Ticker: ')
        date_from = input('Date From (YYYY-MM-DD): ')
        region = RegionSelector()
        time_interval = input('Time interval (1m/30m/1h/1d/1wk/1mo): ')
        SingleStockRawData(folder_path, ticker, date_from, region, time_interval)
        print('\nComplete\n')
    
    elif options == '2':
        stock_list_file_path = input('Stock List File Path(.txt): ')
        folder_path = input('Destination Folder Path: ')
        date_from = input('Date From (YYYY-MM-DD): ')
        region = RegionSelector()
        time_interval = input('Time interval (1m/30m/1h/1d/1wk/1mo): ')
        StockListRawData(stock_list_file_path, folder_path, date_from, region, time_interval)
        print('\nComplete\n')
    
    else:
        print('Incorrect Input, Try Again\n')
        ToolSelector()


print('''
██╗   ██╗ █████╗ ██╗  ██╗ ██████╗  ██████╗     ███████╗██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗    ██╗   ██╗ ██╗███████╗
╚██╗ ██╔╝██╔══██╗██║  ██║██╔═══██╗██╔═══██╗    ██╔════╝██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝    ██║   ██║███║╚════██║
 ╚████╔╝ ███████║███████║██║   ██║██║   ██║    █████╗  ██║██╔██╗ ██║███████║██╔██╗ ██║██║     █████╗         ██║   ██║   ██║██║   ██║██║     ███████╗    ██║   ██║╚██║    ██╔╝
  ╚██╔╝  ██╔══██║██╔══██║██║   ██║██║   ██║    ██╔══╝  ██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██╔══╝         ██║   ██║   ██║██║   ██║██║     ╚════██║    ╚██╗ ██╔╝ ██║   ██╔╝ 
   ██║   ██║  ██║██║  ██║╚██████╔╝╚██████╔╝    ██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗███████╗       ██║   ╚██████╔╝╚██████╔╝███████╗███████║     ╚████╔╝  ██║██╗██║  
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝      ╚═══╝   ╚═╝╚═╝╚═╝  
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n''')

ToolSelector()


