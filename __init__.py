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

def bar(df, col, color, title):
    g = df.sort_values(col, axis = 0)
    x = g['Symbol']
    y1 = g[col]

    trace1 = go.Bar(x=x,y=y1, marker=dict(color=color))

    data = [trace1]

    layout = go.Layout(title=title, barmode="stack",
                      xaxis = dict(tickangle = 90,
                                  showticklabels = True,
                                  type = "category",
                                  dtick = 1))
    fig = go.Figure(data=data,layout=layout)
    fig.show()


def candle(ticker,period='5d',interval='5m'):
    #Interval required 5 minutes
    data = yf.download(tickers=ticker, period=period, interval=interval)
    
    #declare figure
    fig = go.Figure()

    #Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'], name = 'market data'))

    # Add titles
    fig.update_layout(
        title=f'{ticker} live share price evolution',
        yaxis_title='Stock Price (USD per Shares)')

    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am 4pm
            # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )
    fig.show()
    
    return data



def ingest(data, num_cols = 7):
    ''' Takes as input a direct copy paste form the "Account" section of
    Robinhood's web portal
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