import pandas_datareader
pandas_datareader.__version__
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandas_datareader import data
from datetime import date
import math
import pandasql as psql
import data.data_functions as d_f



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
        
        open_initial_value_col_name = ticker + '_open_initial_value'
        open_closing_value_col_name = ticker + '_open_closing_value'
        open_profit_nominal_col_name = ticker + '_open_profit_nominal' 
        open_profit_rate_col_name = ticker + '_open_profit_rate'
        
        closed_initial_value_col_name = ticker + '_closed_initial_value'
        closed_closing_value_col_name = ticker + '_closed_closing_value'
        closed_profit_nominal_col_name = ticker + '_closed_profit_nominal'
        closed_profit_rate_col_name = ticker + '_closed_profit_rate'

        total_initial_value_col_name = ticker + '_total_initial_value'
        total_closing_value_col_name = ticker + '_total_closing_value'
        total_profit_nominal_col_name = ticker + '_total_profit_nominal'
        total_profit_rate_col_name = ticker + '_total_profit_rate'


        yahoo_data[open_initial_value_col_name] = math.nan
        yahoo_data[open_closing_value_col_name] = math.nan
        yahoo_data[open_profit_nominal_col_name] = math.nan
        yahoo_data[open_profit_rate_col_name] = math.nan
        
        yahoo_data[closed_initial_value_col_name] = 0
        yahoo_data[closed_closing_value_col_name] = 0
        yahoo_data[closed_profit_nominal_col_name] = math.nan
        yahoo_data[closed_profit_rate_col_name] = math.nan
        
        yahoo_data[total_initial_value_col_name] = math.nan
        yahoo_data[total_closing_value_col_name] = math.nan
        yahoo_data[total_profit_nominal_col_name] = math.nan
        yahoo_data[total_profit_rate_col_name] = math.nan
        

        quantity = 0
        value = 0

        
        for i in range(0, len(initial_data[ticker])):
            purchase_date = initial_data[ticker][i]['date']
            quantity = quantity + initial_data[ticker][i]['quantity']
            price = initial_data[ticker][i]['price']

            initial_price_of_sold_stocks = -1
            if (initial_data[ticker][i]['quantity'] < 0):
                initial_price_of_sold_stocks = 0
                neg_quantity = initial_data[ticker][i]['quantity'] # -30
                for k in range(0, len(initial_data[ticker])):
                    if ((initial_data[ticker][k]['is_empty'] ==0) & (neg_quantity < 0)):

                        iter_quantity = initial_data[ticker][k]['quantity'] #7.45

                        leftover_quantity =  neg_quantity + iter_quantity  # -22.55
                        

                        if (leftover_quantity > 0):
                            initial_price_of_sold_stocks = initial_price_of_sold_stocks + initial_data[
                                ticker][k]['price'] * neg_quantity

                            initial_data[ticker][k]['quantity'] = leftover_quantity

                        else:
                            initial_price_of_sold_stocks = initial_price_of_sold_stocks + (-initial_data[ticker][k]['value'])   
                            initial_data[ticker][k]['is_empty'] = 1
                            
                        neg_quantity = leftover_quantity 


                            
                value = value + initial_price_of_sold_stocks
                yahoo_data[open_initial_value_col_name].loc[
                                yahoo_data['Date']>=purchase_date] = yahoo_data[open_initial_value_col_name].loc[
                                yahoo_data['Date']>=purchase_date].apply(lambda x: value)

                
                yahoo_data[closed_initial_value_col_name].loc[
                                yahoo_data['Date']>=purchase_date] = yahoo_data[closed_initial_value_col_name].loc[
                                yahoo_data['Date']>=purchase_date].apply(lambda x: x + (-initial_price_of_sold_stocks))
                
                yahoo_data[closed_closing_value_col_name].loc[
                                yahoo_data['Date']>=purchase_date] = yahoo_data[closed_closing_value_col_name].loc[
                                yahoo_data['Date']>=purchase_date].apply(lambda x: x + (-(initial_data[ticker][i]['value'])))
            
                
            else:
                value = value + initial_data[ticker][i]['value']
                yahoo_data[open_initial_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[open_initial_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: value)


            yahoo_data[open_closing_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[ticker].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: x * quantity)
        
            if ticker == '1810.HK':
                yahoo_data[open_closing_value_col_name] = yahoo_data[open_closing_value_col_name].apply(
                lambda x: x*0.1287)

            yahoo_data[open_profit_nominal_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[open_closing_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: x - value)

            yahoo_data[open_profit_rate_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[open_closing_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: 100*(x - value)/value)
            
            # Adding closed positions
            yahoo_data[closed_profit_nominal_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[closed_closing_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date] - yahoo_data[closed_initial_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date]
            
            yahoo_data[closed_profit_rate_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[closed_profit_nominal_col_name].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: x*100) / yahoo_data[closed_initial_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date]
            # Adding totals
            yahoo_data[total_initial_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[open_initial_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date] + yahoo_data[closed_initial_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date]

            yahoo_data[total_closing_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[open_closing_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date] + yahoo_data[closed_closing_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date]

            yahoo_data[total_profit_nominal_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[total_closing_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date] - yahoo_data[total_initial_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date]

            yahoo_data[total_profit_rate_col_name].loc[
                            yahoo_data['Date']>=purchase_date] = yahoo_data[total_profit_nominal_col_name].loc[
                            yahoo_data['Date']>=purchase_date].apply(lambda x: x*100) / yahoo_data[total_initial_value_col_name].loc[
                            yahoo_data['Date']>=purchase_date]
        
    return yahoo_data


def calc_daily_sums(yahoo_data, initial_data):
    '''
    The funtion adds the daily sum value of initial investment, current value of investment,
    nominal profit and profit percentage for each date. 
    Additionally, it removes the records with null values.
    '''
    
    open_initial_value_headers = d_f.get_ticker_headers(initial_data, '_open_initial_value')
    open_closing_value_headers = d_f.get_ticker_headers(initial_data, '_open_closing_value')
    open_profit_nominal_headers = d_f.get_ticker_headers(initial_data, '_open_profit_nominal')
    open_profit_rate_headers = d_f.get_ticker_headers(initial_data, '_open_profit_rate')

    closed_initial_value_headers = d_f.get_ticker_headers(initial_data, '_closed_initial_value')
    closed_closing_value_headers = d_f.get_ticker_headers(initial_data, '_closed_closing_value')
    closed_profit_nominal_headers = d_f.get_ticker_headers(initial_data, '_closed_profit_nominal')
    closed_profit_rate_headers = d_f.get_ticker_headers(initial_data, '_closed_profit_rate')

    total_initial_value_headers = d_f.get_ticker_headers(initial_data, '_total_initial_value')
    total_closing_value_headers = d_f.get_ticker_headers(initial_data, '_total_closing_value')
    total_profit_nominal_headers = d_f.get_ticker_headers(initial_data, '_total_profit_nominal')
    total_profit_rate_headers = d_f.get_ticker_headers(initial_data, '_total_profit_rate')



    yahoo_data['open_initial_value_for_date'] = math.nan
    yahoo_data['open_closing_value_for_date'] = math.nan
    yahoo_data['open_profit_nominal_for_date'] = math.nan
    yahoo_data['open_profit_rate_for_date'] = math.nan

    yahoo_data['closed_initial_value_for_date'] = math.nan
    yahoo_data['closed_closing_value_for_date'] = math.nan
    yahoo_data['closed_profit_nominal_for_date'] = math.nan
    yahoo_data['closed_profit_rate_for_date'] = math.nan

    yahoo_data['total_initial_value_for_date'] = math.nan
    yahoo_data['total_closing_value_for_date'] = math.nan
    yahoo_data['total_profit_nominal_for_date'] = math.nan
    yahoo_data['total_profit_rate_for_date'] = math.nan


    
    for i in range(0, len(yahoo_data)):
        yahoo_data['open_initial_value_for_date'].loc[i] = yahoo_data[open_initial_value_headers].loc[i].sum().sum()
        yahoo_data['open_closing_value_for_date'].loc[i] = yahoo_data[open_closing_value_headers].loc[i].sum().sum()
        yahoo_data['open_profit_nominal_for_date'].loc[i] = yahoo_data[open_profit_nominal_headers].loc[i].sum().sum()
        yahoo_data['open_profit_rate_for_date'].loc[i] = 100 * (
            yahoo_data['open_closing_value_for_date'].loc[i] - yahoo_data['open_initial_value_for_date'].loc[i]
            ) / yahoo_data['open_initial_value_for_date'].loc[i]

        yahoo_data['closed_initial_value_for_date'].loc[i] = yahoo_data[closed_initial_value_headers].loc[i].sum().sum()
        yahoo_data['closed_closing_value_for_date'].loc[i] = yahoo_data[closed_closing_value_headers].loc[i].sum().sum()
        yahoo_data['closed_profit_nominal_for_date'].loc[i] = yahoo_data[closed_profit_nominal_headers].loc[i].sum().sum()
        yahoo_data['closed_profit_rate_for_date'].loc[i] = 100 * (
            yahoo_data['closed_closing_value_for_date'].loc[i] - yahoo_data['closed_initial_value_for_date'].loc[i]
            ) / yahoo_data['closed_initial_value_for_date'].loc[i]

        yahoo_data['total_initial_value_for_date'].loc[i] = yahoo_data[total_initial_value_headers].loc[i].sum().sum()
        yahoo_data['total_closing_value_for_date'].loc[i] = yahoo_data[total_closing_value_headers].loc[i].sum().sum()
        yahoo_data['total_profit_nominal_for_date'].loc[i] = yahoo_data[total_profit_nominal_headers].loc[i].sum().sum()
        yahoo_data['total_profit_rate_for_date'].loc[i] = 100 * (
            yahoo_data['total_closing_value_for_date'].loc[i] - yahoo_data['total_initial_value_for_date'].loc[i]
            ) / yahoo_data['total_initial_value_for_date'].loc[i]

    first_ticker = d_f.get_ticker_names(initial_data)[0]
    yahoo_data = yahoo_data[yahoo_data[first_ticker].isnull()==False]
    return yahoo_data

def fill_df_with_past(_initial_stocks, _df_dates, _stocks_data):

    q = """
    SELECT SUBSTRING(A.DateCol, 0, 11) AS Date, """ + d_f.generate_select_tickers(d_f.get_ticker_names(_initial_stocks)) + """
    FROM _df_dates AS A
    LEFT JOIN _stocks_data AS B
    ON A.DateCol = B.Date
    LEFT JOIN _stocks_data AS B_1
    ON Date(SUBSTRING(A.DateCol, 0, 11)) = Date(SUBSTRING(B_1.Date, 0, 11), '+1 day')
    LEFT JOIN _stocks_data AS B_2
    ON Date(SUBSTRING(A.DateCol, 0, 11)) = Date(SUBSTRING(B_2.Date, 0, 11), '+2 day')
    LEFT JOIN _stocks_data AS B_3
    ON Date(SUBSTRING(A.DateCol, 0, 11)) = Date(SUBSTRING(B_3.Date, 0, 11), '+3 day')
    """
    return psql.sqldf(q, locals())

def run_data_load(_initial_stocks):
    stocks_data = get_yahoo_data(
        d_f.get_ticker_names(_initial_stocks)
        , d_f.get_min_date(_initial_stocks)
        , date.today())
    
    df_dates = pd.DataFrame(pd.date_range(d_f.get_min_date(_initial_stocks), date.today()), columns = ['DateCol'])

    stocks_data_filled = fill_df_with_past(_initial_stocks, df_dates, stocks_data)
    stocks_data_filled['Date'] = pd.to_datetime(stocks_data_filled['Date'])


    stocks_data_calc = update_yahoo_data(stocks_data_filled, _initial_stocks)
    final_stocks_data = calc_daily_sums(stocks_data_calc, _initial_stocks)
    final_stocks_data.to_csv('data/mystocks.csv')

