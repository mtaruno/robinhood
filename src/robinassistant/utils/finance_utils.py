'''
Useful utilities for financial data.

The philosophy behind a utilities file is that the entire team works on this
script as if this is "sacred" meaning that we don't change stuff here and there
here and that the modules created here are correct, tested, and should be the 
consistent.

'''

import pandas_datareader.data as web
import datetime
import pandas as pd
import warnings


def price_action(ticker: str, token_path = "resources/token.txt", 
    start_date: datetime.date = datetime.date(2021,1,1)
    , end_date: datetime.date = datetime.datetime.today()) -> pd.DataFrame:
    ''' Retrieve the price action data for a stock given a time period.

    Note that the APIs are constantly changing,
    so it may break from time to time.

    https://pandas-datareader.readthedocs.io/en/latest/remote_data.html

    Default: From Jan 1 2021 to Today

    '''
    with open(token_path) as f:
        token = f.readline()

    print(start_date.weekday())

    if start_date.weekday() in [5,6]:
        warnings.warn("The Start Date is not a weekday! Market probably has no data there.")

    price_data = pd.DataFrame()

    try:
        price_data = web.get_data_tiingo(
            ticker, start=start_date, end=end_date, api_key=token)
    except KeyError:
        print("Not available for the dates specified")

    return price_data

def multi_price_action(tickers: list, token_path = 'resources/token.txt', start_date: datetime.date = datetime.date(2021,1,1)
    , end_date: datetime.date = datetime.datetime.today()) -> dict:
    ''' We want to ingest price action data for multiple tickers at once
    
    Returns a dictionary with successful fetches of tickers in the keys and
    the stock action data in the values. 
    '''
    with open(token_path) as f:
        token = f.readline()

    failed = []
    passed = {}

    # testing if fetching data will invoke an error
    for tick in tickers:
        try:
            passed[tick] = web.get_data_tiingo(
                tick, start=start_date, end=end_date, api_key=token)
        except (IOError, KeyError):
            print(f'Failed to read symbol: {tick}, will replace with NaN.')
            failed.append(tick)

    # reporting
    if failed: # means failed list contains any element at all
        print("Data not available for following tick/tickers: {}".format(str(failed)))

    return passed

def price_action_with_retries(ticker, token_path = "token.txt", 
    start_date: datetime.date = datetime.date(2021,1,1)
    , end_date: datetime.date = datetime.datetime.today()) -> pd.DataFrame:
 
    with open(token_path) as f:
        token = f.readline()

    # I want to code to increment backwards by a day until it finds a day with a valid date
    # ~ max tries are one week back to look for available data
    for _ in range(8):    
        try:
            price_data = web.get_data_tiingo(
                ticker, start=start_date, end=end_date, api_key=token
            )
        except KeyError as e:
            print(f"Data Unavailable for {str(start_date)}")
            start_date = start_date - datetime.timedelta(1)

    return price_data



def rsi(df: pd.DataFrame, periods = 14, ema = True) -> pd.DataFrame:
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

