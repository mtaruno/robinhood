#%%
import pandas as pd
import numpy as np
import re
import seaborn as sns
# Data Source
import ingest
from datetime import datetime

# Colors
c = dict(gold = "#FFD700", silver = "#CD7F32", bronze = "#9EA0A1")

#%%
import os
os.listdir()
# %%
with open('../data/stocks.txt') as f:
    raw = f.read()
    
df = ingest.ingest(raw)
#%%
# Dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
# Add an import for pandas_datareader and datetime
import pandas_datareader.data as web


# %%
cat = {}
cat['energy'] = ['']
cat['momentum'] = []
cat['watchlist'] = ["CLOV", "CCIV"]
cat['research_more'] = [""]
cat['sus'] = ["BNGO", ""]


format_dict = {'Percentage': '{:.2%}', 'Decay/Increase': '{:.2%}'} # 'sum':'${0:,.0f}', 'date': '{:%m-%Y}', 

# seeing my portfolio
show = lambda x: x.style.set_properties(**{'background-color': 
    'black','color': 'lawngreen','border-color': 'white'})\
.applymap(lambda x: f"color: {'cyan' if isinstance(x,str) else 'lawngreen'}")\
.background_gradient(cmap='Purples')\
.format(format_dict)
show(df)

# %%
import visualize

visual_sort = lambda df, col : df.sort_values(col)

visualize.bar(x = df.sort_values('Total Return')['Symbol'], 
        y = df.sort_values('Total Return')['Total Return'], 
        color = c["gold"], title = "Total Returns")
visualize.bar(x = df.sort_values("Percentage")['Symbol'], 
      y = df.sort_values("Percentage")['Percentage'], color = c["silver"], 
      title = "Percentage of Holdings")
visualize.bar(x = df.sort_values("Decay/Increase")['Symbol'], 
      y = df.sort_values("Decay/Increase")['Decay/Increase'],
      color = c["bronze"], title = "Stock Performances Since Avg Cost")


# %%

# adding technical indicators

# finding RSI for each ticker
import f_utils

ticker = "TSLA"
start_date = '2021-01-01'
end_date = '2021-06-13'

# using f_utils to get price action data for a specified ticker
price_data = f_utils.price_action(ticker= ticker, start_date=start_date,
end_date=end_date)

price_data

# getting the 30 RSI for all the stocks
# visualize.single_line(x = , y = stock['rsi_14'], 
# title = f"{ticker} RSI30")


# %%


d_rsi = f_utils.rsi(data)
single_line(x = data['date'], y = d_rsi)
# %%

# %%