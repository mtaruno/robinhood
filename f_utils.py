'''
Useful utilities for financial data.

The philosophy behind a utilities file is that the entire team works on this
script as if this is "sacred" meaning that we don't change stuff here and there
here and that the modules created here are correct, tested, and should be the 
consistent.

'''

def price_action(ticker, start_date = "2021-01-01", end_date = str(datetime.date.today())):
    ''' Retrieve the price action data for a stock given a time period.

    Default: From Jan 1 2021 to Today
    '''
    from pandas_datareader import data as pdr
    from datetime import datetime
    
    pdr.get_data_yahoo(ticker, start = 
    start_date, end= end_date)



def rsi(df, periods = 14, ema = True):
    """
    Returns a pd.Series with the relative strength index give a price action
    dataframe.
    """
    close_delta = df['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi