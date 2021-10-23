import pandas_datareader
pandas_datareader.__version__
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
from pandas_datareader import data
from datetime import date


initial_stocks = {
    'MSFT':[{'price': 210.99, 'quantity': 5, 'value': 1054.95, 'date': '2020-11-23'}],
    'AMZN':[{'price': 3250.0, 'quantity': 1, 'value': 3250, 'date': '2020-12-02'}],
    'SNOW': [{'price': 334.84, 'quantity': 0.153, 'value': 51.41, 'date': '2020-12-24'},
             {'price': 215.19, 'quantity': 4, 'value': 860, 'date': '2021-03-25'}],
    'BABA': [{'price': 275.0, 'quantity': 5, 'value': 1375,'date': '2020-11-25'},
             {'price': 200, 'quantity': 2, 'value': 400, 'date': '2021-07-08'}],
    'MU': [{'price': 76.71, 'quantity': 5, 'value': 383.55, 'date': '2021-07-08'}],
    'BNGO': [{'price': 5.97, 'quantity': 58.63, 'value': 350, 'date': '2021-07-15'}],
    'FSLY': [{'price': 64.88, 'quantity': 4.62, 'value': 300, 'date': '2021-03-04'}],
    'BIDU': [{'price': 213.38, 'quantity': 1.3, 'value': 277.84, 'date': '2021-03-25'}],
    'NNDM': [{'price': 9.26, 'quantity': 7.45, 'value': 69, 'date': '2020-12-24'},
             {'price': 10.62, 'quantity': 4.72, 'value': 50, 'date': '2021-02-25'},
             {'price': 8.72, 'quantity': 34.4, 'value': 300, 'date': '2021-03-25'},
             {'price': 6.97, 'quantity': 33.92, 'value': 236.45, 'date': '2021-04-15'}],
    'FSLR': [{'price': 74.98, 'quantity': 2.67, 'value': 200, 'date': '2021-03-04'}],
    'CRM': [{'price': 242, 'quantity': 0.785, 'value': 190, 'date': '2020-12-01'}],
    'SUMO': [{'price': 26.36, 'quantity': 6.83, 'value': 180, 'date': '2021-03-04'},
             {'price': 19.15, 'quantity': 6.15, 'value': 117.73, 'date': '2021-04-08'}],
    'XPEV': [{'price': 39.68, 'quantity': 3.83, 'value': 152, 'date': '2021-07-08'}],
    'FROG': [{'price': 46.72, 'quantity': 3.24, 'value': 151.6, 'date': '2021-03-04'}],
    'SPLK': [{'price': 140.46, 'quantity': 1.07, 'value': 150, 'date': '2021-03-04'}],
    'U': [{'price': 125.7, 'quantity': 0.96, 'value': 120.53, 'date': '2021-02-11'},
          {'price': 90.99, 'quantity': 2.09, 'value': 190, 'date': '2021-03-25'}],
    '1810.HK': [{'price': 25.9, 'quantity': 30, 'value': 100.24, 'date': '2020-11-30'}],
    'NVDA': [{'price': 123.31, 'quantity': 0.81, 'value': 100, 'date': '2020-11-30'},
             {'price': 143.75, 'quantity': 0.7, 'value': 100, 'date': '2021-03-04'}],
    'TSLA': [{'price': 602.48, 'quantity': 0.083, 'value': 50, 'date': '2020-11-30'},
             {'price': 607.8, 'quantity': 0.1646, 'value': 100, 'date': '2021-03-04'},
             {'price': 612.22, 'quantity': 0.1635, 'value': 100, 'date': '2021-03-05'}],
    'CSCO': [{'price': 46.02, 'quantity': 1.72, 'value': 79.06, 'date': '2021-02-18'},
             {'price': 45.68, 'quantity': 1.55, 'value': 70.81, 'date': '2021-02-25'}],
    'AAPL': [{'price': 135.28, 'quantity': 0.53, 'value': 72, 'date': '2021-02-04'}],
    'GOOG': [{'price': 1874.87, 'quantity': 0.0385, 'value': 71.8, 'date': '2021-01-28'}],
    'TWLO': [{'price': 348.61, 'quantity': 0.174, 'value': 60.6, 'date': '2021-01-07'},
             {'price': 399.48, 'quantity': 5, 'value': 1997.4, 'date': '2021-03-01'},
             {'price': 343.32, 'quantity': 0.2037, 'value': 70, 'date': '2021-03-04'}],
    'SPOT': [{'price': 306, 'quantity': 0.196, 'value': 59.91, 'date': '2021-02-26'}],
    'MDB': [{'price': 402.58, 'quantity': 0.14, 'value': 55, 'date': '2021-02-04'}],
    'DASH': [{'price': 179.9, 'quantity': 0.29, 'value': 52.7, 'date': '2020-12-10'}],
    'NIO': [{'price': 54.14, 'quantity': 0.92, 'value': 50, 'date': '2020-11-30'}],
    'QCOM': [{'price': 144.73, 'quantity': 0.35, 'value': 50, 'date': '2020-11-30'},
            {'price': 132.91, 'quantity': 0.75, 'value': 100, 'date': '2021-02-18'}],
    'AMD': [{'price': 87.62, 'quantity': 0.57, 'value': 50, 'date': '2021-02-04'}],
}


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

def get_yahoo_data(tickers, start_date, end_date):
    '''
    returns the historical prices of the stocks given in the "tickers" input parameter.
    bounds the historical values with "start_date" and "end_date" parameters.
    result of the function is a pandas dataframe
    '''
    yahoo_result = data.get_data_yahoo(tickers, start_date, end_date).reset_index()[['Close', 'Date']].copy()
    yahoo_result.columns = yahoo_result.columns.droplevel()
    yahoo_result = yahoo_result.rename(columns = {'':'Date'})
    return yahoo_result

def update_yahoo_data(yahoo_data, initial_data):
    '''
    function takes yahoo historical data and adds the static initial purchase price and quantity
    to the dataframe, additionally, calculates and adds the total initial 
    and total current values of the stocks based on the quantity of the bought stocks.
    result of the function is a pandas dataframe
    '''

    for ticker in initial_data:
        initial_price_total_col_name = ticker + '_initial_total'
        current_total_price_col_name = ticker + '_current_total'
        profit_nominal_col_name = ticker + '_profit_nominal' 
        profit_rate_col_name = ticker + '_profit_rate'

        yahoo_data[initial_price_total_col_name] = np.NaN
        yahoo_data[current_total_price_col_name] = np.NaN
        yahoo_data[profit_nominal_col_name] = np.NaN
        yahoo_data[profit_rate_col_name] = np.NaN

        quantity = 0
        value = 0
        
        for i in range(0, len(initial_data[ticker])):
            purchase_date = initial_data[ticker][i]['date']
            quantity = quantity + initial_data[ticker][i]['quantity']
            price = initial_data[ticker][i]['price']
            value = value + initial_data[ticker][i]['value']

            yahoo_data[initial_price_total_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[ticker].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: value)
            
            yahoo_data[current_total_price_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[ticker].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: x * quantity)
            
            if ticker == '1810.HK':
                yahoo_data[current_total_price_col_name] = yahoo_data[current_total_price_col_name].apply(
                lambda x: x*0.1287)
   
            yahoo_data[profit_nominal_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[current_total_price_col_name].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: x - value)
            yahoo_data[profit_rate_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[current_total_price_col_name].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: 100*(x - value)/value)
        
    return yahoo_data


def calc_daily_sums(yahoo_data, initial_data):
    '''
    The funtion adds the daily sum value of initial investment, current value of investment,
    nominal profit and profit percentage for each date. 
    Additionally, it removes the records with null values.
    '''
    
    initial_value_headers = get_ticker_headers(initial_data, '_initial_total')
    current_value_headers = get_ticker_headers(initial_data, '_current_total')
    profit_nominal_headers = get_ticker_headers(initial_data, '_profit_nominal')
    profit_rate_headers = get_ticker_headers(initial_data, '_profit_rate')
    
    yahoo_data['initial_value_for_date'] = np.NaN
    yahoo_data['current_value_for_date'] = np.NaN
    yahoo_data['profit_nominal_for_date'] = np.NaN
    yahoo_data['profit_rate_for_date'] = np.NaN
    
    for i in range(0, len(yahoo_data)):
        yahoo_data['initial_value_for_date'].loc[i] = yahoo_data[initial_value_headers].loc[i].sum().sum()
        yahoo_data['current_value_for_date'].loc[i] = yahoo_data[current_value_headers].loc[i].sum().sum()
        yahoo_data['profit_nominal_for_date'].loc[i] = yahoo_data[profit_nominal_headers].loc[i].sum().sum()
        yahoo_data['profit_rate_for_date'].loc[i] = 100 * (
            yahoo_data['current_value_for_date'].loc[i] - yahoo_data['initial_value_for_date'].loc[i]
            ) / yahoo_data['initial_value_for_date'].loc[i]

    yahoo_data = yahoo_data[yahoo_data['SNOW'].isnull()==False]
    return yahoo_data

stocks_data = get_yahoo_data(
      get_ticker_names(initial_stocks)
    , get_min_date(initial_stocks)
    , date.today())

stocks_data_calc = update_yahoo_data(stocks_data, initial_stocks)

final_stocks_data = calc_daily_sums(stocks_data_calc, initial_stocks)
final_stocks_data.to_csv('mystocks.csv')

