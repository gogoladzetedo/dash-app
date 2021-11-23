import pandas as pd
import json
import io
import base64
import pandas_datareader
pandas_datareader.__version__
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandas_datareader import data
from datetime import date
import pandasql as psql



def get_min_date(obj):
    '''
    returns the earliest date when the transaction was made, i.e. first date in the input dictionary
    '''
    
    min_date = '2039-01-01'
    for ticker in obj:
        curr_date = obj[ticker][0]['date']
        if curr_date < min_date:
            min_date = curr_date
    return min_date
    
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
    with open('data/initial_positions.json') as json_file:
        init_file = json.load(json_file)
    return init_file

def generate_select_tickers(tickers_list):
    res = ''
    for row_n, tick in enumerate(tickers_list):
        if row_n == 0:
            res = res + ''
        else:
            res = res + ', '
        res = res + 'COALESCE(B.'+tick+', B_1.'+tick+', B_2.'+tick+', B_3.'+tick+') AS '+tick
    return res

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), header = None)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return 'There was an error processing this file.'
    return df

def rename_df_columns(df):
    df.columns = ['name', 'date', 'price', 'quantity'] 
    return df

def df_to_dict(df):
    all_stocks = {}
    for _index, _row in df.iterrows():

        current_stock = {}

        current_stock['price'] = _row['price']
        current_stock['quantity'] = _row['quantity']
        current_stock['value'] = _row['price'] * _row['quantity']
        current_stock['date'] = _row['date']
        current_stock['is_empty'] = 0

        if _row['name'] in all_stocks:
            added_current_stock = all_stocks[_row['name']].copy()
            added_current_stock.append(current_stock)
        else:
            added_current_stock = []
            added_current_stock.append(current_stock)

        all_stocks[_row['name']] = added_current_stock
    return all_stocks
