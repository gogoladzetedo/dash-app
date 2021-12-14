

# Idea: Add your portfolio - Certain amount of purchased and sold stocks and cryptos 
# Goal: You know exactly how much profit/loss you have for every day from the beginning of the purchases, 
# You know major contributors in that, and you know which of your stocks are performing better or worse. 

# Define the metrics:

# Metrics for individual company stock level:
# - (Comparison of) Daily Profit/Loss from stocks for each stock ticker, based on the position open/closed status
# , shown as nominal and as the rate. 
#       
# Daily stock performance - Current value of the stocks (compared to the initial investment amount, what you paid for them) 
# , for each Stock ticker, based on the position open/closed status. 

# Total metrics - based on all the company stocks: 
# Total investments, based on the position open/closed status, daily 

# Total profits, based on the position open/closed status, daily
# , shown as nominal and as the rate. Example:

# Share of stocks - proportions of each stock compared to the whole, based on the position open/closed status
# Shown in current value figures, or in the initial investment figures.


# Example:
#       Bought 10 Tesla stocks and 5 Apple stocks. After two weeks, bough 5 more Tesla. After three weeks, sold 12 Tesla stocks.



# Current format of dataset from pandas_datareader API formatted in our own way 
# has Daily records (except for the holidays and weekends), so everyday there's a closing value of each and every stock of ours.

from pandas_datareader import data
def flatten_df(df):
    res_df = df
    res_df = res_df.reset_index()
    res_df = res_df[['Close', 'Date']]
    res_df.columns.droplevel()
    res_df.columns = res_df.columns.droplevel()
    res_df = res_df.rename(columns = {'':'Date'})
    return res_df
tickers = ['TSLA', 'AAPL']
df = data.get_data_yahoo(tickers, '2021-08-01', '2021-09-30')
df_clean = flatten_df(df)

print(df_clean.head(20))
print('\n', df_clean.tail(20))

# These are the official closing prices of the stocks. Now,
#   Let's say, on 2021-08-05 you Bought 10 stocks of Tesla priced as 711$ each (total 7110$), 
# and 10 stocks of Apple at 146.5$ each (total, 1465$). 
#   After one week, in 2021-08-12, you bought 5 more Tesla stock, each priced as 685$ (total 3225$)
#   After a while, in 2021-09-27, you sold 12 Tesla stocks each at 785$, totalling 9420 $.

# Our goal is to calculate the above mentioned metrics for your stocks.
# Like, how was your daily portfolio performing or how much was the profit or loss

# Basic concepts to introduce here: Initial investment value - value that you paid for the stock.
# Closing / Current value - value for the given date. 
# Initial value for the stock is constant until the next purchase / sell operation. 
# In this case, Initial value of owned Tesla stocks is 7110$ from 2021-08-05 until 2021-08-12. 
# At that point, after buying more, it becomees 7110$ + 3425$ = 10535$ . 
# The value stays the same until 2021-09-27, when 12 stocks are sold. Here, for calculating the leftover initial value, 
# we need a FIFO (First-In-First-Out) method: so we need to substract the purchasing amounts of the stocks:
#  - 10 of them from the first trade (initial value was 7110$) and two of them from the 
# second trade (2*685 $ = 1370 $), so the purchasing cost or the initial value of the 
# 12 Tesla stocks that we just sold was 7110$ + 1370$ = 8480$ (sold for 9420$, you made a good profit, yay!)
# , That means the currently open positions for Tesla are only 3 stocks,
# and the initial value / purchased price for them is 3 * 685$ = 2055$ (mentionother way of calculating)

# split these amounts into 3 horizontal categories - open positions, closed positions, total.
