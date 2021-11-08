import pandas as pd
import json

def get_ticker_names(obj):
    '''
    returns the ticker names as the list from the input dictionary
    '''
    tickers = []
    for ticker in obj:
        tickers.append(ticker)
    return tickers

def get_ticker_headers(initial_data, header_suffix):
    '''
    generates the new column names by adding the input suffix to the stock ticker
    '''
    nominal_profit_headers = []
    for ticker in initial_data:
        header_name = ticker + header_suffix
        nominal_profit_headers.append(header_name)
    return nominal_profit_headers

def input_file(filename):
    return pd.read_csv(filename)



def initial_stocks():
    with open('initial_positions.json') as json_file:
        init_file = json.load(json_file)
    return init_file

