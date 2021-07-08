'''
Multiple stocks dropdown 
'''
#%%
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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

portfolio = ['TSLA', 'PLTR', 'JMIA']
names = ['Tesla', 'Palantir', 'Jumia']

options = []

for tic, name in zip(portfolio, names):
    mydict = {} # label: user sees, value: script sees
    mydict['label'] = tic + ' ' + name
    mydict['value'] = tic
    options.append(mydict)

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([html.H3('Enter a stock symbol:', 
    style = {
        'paddingRight':'30px'}), 
    dcc.Dropdown(
        id='my_ticker_symbol',
        options=options,
        value = ['TSLA'],
        multi = True
        )
    ], style = {'display': 'inline-block','verticalAlign': 'top',
'width': '30%'}
        ),
    html.Div([html.H3('Select a start and end date'),
        dcc.DatePickerRange(id='my_date_picker',
        min_date_allowed = datetime(2021,1,1),
        max_date_allowed = datetime.today(),
        start_date = datetime(2021,1,1),
        end_date = datetime.today()
    )], style = {'display': 'inline-block'}),
    html.Div([
        html.Button(id='submit-button',
        n_clicks=0,
        children='Submit',
        style={'fontSize': 24, 'marginLeft': '30px'})
    ])
    ,
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
])
@app.callback(Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'), 
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    # Use datareader and datetime to define a DataFrame
    start = datetime.strptime(str(start_date)[:10], '%Y-%m-%d'),
    end = datetime.strptime(str(end_date)[:10], '%Y-%m-%d')

    # creating trace for every stock ticker
    traces = []
    for tic in stock_ticker:
        df = price_action(tic, token_path = "../token.txt", start_date = start, end_date = end)
        traces.append({
            'x':df.reset_index()['date'],
            'y': df['close'], 'name': tic
        })

    # change the output data
    fig = {
        'data': traces,
        'layout': {'title': ', '.join(stock_ticker) + ' Closing Prices'}
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

start_date = str(datetime(2021,1,1))
end_date = str(datetime.today())
start = datetime.strptime(start_date[:10], '%Y-%m-%d')
end = datetime.strptime(end_date[:10], '%Y-%m-%d')
df = price_action('TSLA', token_path = "../token.txt", start_date = start_date, end_date = end_date)

# %%
df
# %%
