import pandas as pd
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



initial_stocks = {
    'SNOW': [{'price': 334.84, 'quantity': 0.153, 'value': 51.41, 'date': '2020-12-24', 'is_empty': 0},
             {'price': 215.19, 'quantity': 4, 'value': 860, 'date': '2021-03-25', 'is_empty': 0}],
    'BABA': [{'price': 275.0, 'quantity': 5, 'value': 1375,'date': '2020-11-25', 'is_empty': 0},
             {'price': 200, 'quantity': 2, 'value': 400, 'date': '2021-07-08', 'is_empty': 0},
             {'price': 280, 'quantity': -5, 'value': -1400, 'date': '2021-07-15', 'is_empty': 0}],
   
    'BIDU': [{'price': 213.38, 'quantity': 1.3, 'value': 277.84, 'date': '2021-03-25', 'is_empty': 0}],
    'NNDM': [{'price': 9.26, 'quantity': 7.45, 'value': 69, 'date': '2020-12-24', 'is_empty': 0},
             {'price': 10.62, 'quantity': 4.72, 'value': 50, 'date': '2021-02-25', 'is_empty': 0},
             {'price': 8.72, 'quantity': 34.4, 'value': 300, 'date': '2021-03-25', 'is_empty': 0},
             {'price': 12.00, 'quantity': -30.00, 'value': -360.00, 'date': '2021-04-01', 'is_empty': 0},
             {'price': 6.97, 'quantity': 33.92, 'value': 236.45, 'date': '2021-04-15', 'is_empty': 0}],
    'FSLR': [{'price': 74.98, 'quantity': 2.67, 'value': 200, 'date': '2021-03-04', 'is_empty': 0}]
}
