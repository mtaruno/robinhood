'''
Adding dates.
'''
#%%
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Add an import for pandas_datareader and datetime
import pandas_datareader.data as web
from datetime import datetime

#%%
def price_action(ticker, token_path = "token.txt", start_date = "2021-01-01", 
end_date = str(datetime.today())):
    ''' Retrieve the price action data for a stock given a time period.

    Note that the APIs are constantly changing,
    so it may break from time to time.

    https://pandas-datareader.readthedocs.io/en/latest/remote_data.html

    Default: From Jan 1 2021 to Today

    '''
    with open(token_path) as f:
        token = f.readline()

    df = web.get_data_tiingo(ticker, start = 
    start_date, end = end_date, api_key = token)

    return df

#%%

app = dash.Dash()

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([html.H3('Enter a stock symbol:', style = {
        'paddingRight':'30px'
    }), dcc.Input(
        id='my_ticker_symbol',
        value='TSLA'
    )]),
    html.Div([html.H3('Select a start and end date'),
    dcc.DatePickerRange(id='my_date_picker',
    min_date_allowed = datetime(2021,1,1),
    max_date_allowed = datetime.today(),
    start_date = datetime(2021,1,1),
    end_date = datetime.today()
    )]),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
])
@app.callback(
    Output('my_graph', 'figure'),
    [Input('my_ticker_symbol', 'value'), 
    Input('my_date_picker', 'start_date'),
    Input('my_date_picker', 'end_date')])
def update_graph(stock_ticker, start_date, end_date):
    # Use datareader and datetime to define a DataFrame
    start = datetime.strptime(start_date[:10], '%Y-%m-%d'),
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    df = price_action(stock_ticker, token_path = "../token.txt", 
    start_date = start, end_date=end)
    # Change the output data
    fig = {
        'data': [
            {'x': df.reset_index()['date'], 'y': df['close']}
        ],
        'layout': {'title':stock_ticker}
    }
    return fig

if __name__ == '__main__':
    app.run_server()
# %%

start = datetime(2020, 1, 1)
end = datetime(2020, 12, 31)
df = price_action('TSLA', token_path = "../token.txt", 
start_date = start, end_date=end)

df
# %%
datetime.today()

# %%
