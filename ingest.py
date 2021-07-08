# This is where I make some useful functions

import plotly.express as px
import seaborn as sns
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd
import numpy as np
import re
from pandas_datareader import data as pdr
import datetime



def ingest(data, num_cols = 7):
    ''' Takes as input a direct copy paste form the "Account" section of
    Robinhood's web portal. Special function for Robinhood.
    '''
    get_data = lambda ticker, start_date = "2021-01-01": pdr.get_data_yahoo(ticker, start = start_date, end=str(datetime.date.today()))
    
    # Storing data in a list - list comprehension is to remove empty strings
    data = [i for i in data.split('\n') if i] 
    counter = 0
    headings = data[:num_cols]
    remainder = data[num_cols:]
    d = {"Name": [], "Symbol": [], "Shares":[], "Price":[], "Average Cost": [],
        "Total Return (Abs)": [], "Equity": []}
    for e in remainder:
        pos = counter%num_cols
        if pos == 0:
            d["Name"].append(e)
        elif pos == 1:
            d["Symbol"].append(e)
        elif pos == 2:
            d["Shares"].append(e)
        elif pos == 3:
            d["Price"].append(e)
        elif pos == 4:
            d["Average Cost"].append(e)
        elif pos == 5:
            d["Total Return (Abs)"].append(e)
        elif pos == 6:
            d['Equity'].append(e)
        
        counter += 1
        
    df = pd.DataFrame(d)
    
    to_float = lambda e: float(re.sub("[^0-9.]", "", e))
    
    to_apply = ['Price', 'Average Cost', 'Total Return (Abs)', 
                'Equity', 'Shares']
    
    for col in to_apply:
        df[col] = df[col].apply(to_float)
        
    # Calculating the most recent price
    price = [get_data(ticker, start_date = str(datetime.date.today())).Close.iloc[-1] for ticker in df['Symbol']]
    df['Price'] = price
    
    # Calculating the correct total return
    df['Total Return'] = df['Shares']*df['Price'] - df['Shares'] * \
    df['Average Cost']
    
    df['Diff'] = abs(df['Total Return']) - abs(df['Total Return (Abs)'])
    
    # Percentage of Total Portfolio
    df['Percentage'] = df['Equity'] / sum(df['Equity'])
    
    # Percentage Change since Bought
    df['Decay/Increase'] = (df['Price'] - df['Average Cost'])/ df['Average Cost']
    
    return df