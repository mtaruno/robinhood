# This is where I make some useful functions
#%%
import os
import plotly.express as px
import seaborn as sns
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd
import numpy as np
import re
import datetime
import f_utils


class ETL:
    def __init__(self):
        self.paths = {'token': "../data/token.txt",
                        'data': "../data/stocks.txt"}

    def ingest_robin_table(self, data: str, num_cols = 7) -> pd.DataFrame:
        ''' Takes as input a direct copy paste form the "Account" section of
        Robinhood's web portal. Special function for Robinhood.
        '''
        # Storing data in a list - list comprehension is 
        # to remove empty strings
        data = [i for i in data.split('\n') if i] 

        # text file specific logic where data is every 7 tokens
        headings = data[:num_cols]
        remainder = data[num_cols:]

        # skeleton of all the columns i care about 
        d = {"Name": [], "Symbol": [], "Shares":[], "Price":[], "Average Cost": [],
            "Total Return (Abs)": [], "Equity": []}

        for counter, e in enumerate(remainder):
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

        df = pd.DataFrame(d)

        # converting text that couldn't be turned to a float and then turning it to float
        to_float = lambda e: float(re.sub("[^0-9.]", "", e))

        cols_to_turn_to_float = ['Price', 'Average Cost', 'Total Return (Abs)', 
                    'Equity', 'Shares']

        for col in cols_to_turn_to_float:
            df[col] = df[col].apply(to_float)

        return df

  
    def additional_robin_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        ''' My column additions on top of the defaults '''
        start_date = datetime.datetime.today() - datetime.timedelta(2)

        # Calculating the most recent price
        prices = f_utils.price_action(df.Symbol, 
        token_path = self.paths['token'], 
        start_date = start_date)


        df['Price'] = [i[0] for i in prices]

        # Calculating the correct total return
        df['Total Return'] = df['Shares']*df['Price'] - df['Shares'] * \
        df['Average Cost']

        df['Diff'] = abs(df['Total Return']) - abs(df['Total Return (Abs)'])

        # Percentage of Total Portfolio
        df['Percentage'] = df['Equity'] / sum(df['Equity'])

        # Percentage Change since Bought
        df['Decay/Increase'] = (df['Price'] - df['Average Cost'])/ df['Average Cost']

        return df

    def get_full_table(self):

        with open(self.paths['data']) as f:
            raw = f.read()

        df = self.ingest_robin_table(data = raw)

        return self.additional_robin_columns(df)