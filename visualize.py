'''
Utilities file for all data visualizations
'''

import plotly.offline as pyo
import plotly.graph_objs as go

def bar(x, y, color, title):
    trace1 = go.Bar(x=x,y=y, marker=dict(color=color))

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


def single_line(x, y, title = 'Line Plot', mode = 'lines', hovertext=None, fill=None):
  ''' A single line graph given x, y, and a title with Plotly '''
  trace = go.Scatter(x = x, y = y, mode = mode, name = 'lines', hovertext = 
  hovertext, fill = fill)
  layout = go.Layout(title = title)
  data = [trace]
  fig = go.Figure(data = data, layout = layout)
  fig.show()