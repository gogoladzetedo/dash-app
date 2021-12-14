from pandas_datareader import data

mylist = [0, 1, 4, 5, 7, 9, 10, 'varx', True, [1, 'x'], 7]

len(mylist)


mylist = [1, 5, 6, 3, 36, 2, 6, 22, 9]

mylist2 = mylist
mylist3 = mylist.copy()
#print(mylist, mylist2, mylist3)

len(mylist)

mylist[0]

mylist.append('new number')

mylist[-1]

mylist[0:2]

mylist.remove(6)

mylist.pop(0)



#print(mylist, mylist2, mylist3)



mydict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
len(mydict)

mydict['b']

mydict['f']=6

mydict.pop('a')

del mydict['b']

mydict['f']=8

mydict['g']=[1, 2, 3, 4, 5]

mydict['g'][0:2]

mydict['h']={'h1': 'x', 'h2': 'y', 'h3': 'z', 'h4': 'Z'}

mydict['h']['h1']=['xyz', {'key1': 10, 'key2': 20}, 'def']

mydict['h']

mydict['h']['h1']

mydict['h']['h1'][1]['key2']


##### File input / output


import os
print (os.getcwd())

# read, pandas
import pandas as pd
df = pd.read_csv('localfile.csv', sep=',')
# write, pandas
df.to_csv('output.csv', index=False)  


 #read, csv
import csv
csv_file_content = []
with open('localfile.csv', 'r') as file:
    csv_reader_rows = csv.reader(file)
    for row in csv_reader_rows:
        csv_file_content.append(row)

# read, file
with open('localfile.csv', 'r') as file:
    csv_content = file.readlines()
print(csv_content[0])

# write, file, json
import json
mydict = {'a': 1, 'b': 2}
with open('newfile.json', 'w') as fp:
    json.dump(mydict, fp, sort_keys=True, indent=4)


# pandas_datareader, pandas operations
from pandas_datareader import data
import math

df = data.get_data_yahoo(['MSFT', 'AMZN', 'TSLA'], '2021-08-01', '2021-09-30')
df = df.reset_index()
df = df[['Close', 'Date']]
df.columns.droplevel()
df.columns = df.columns.droplevel()
df = df.rename(columns = {'':'Date'})



df['new_col'] = 0
df['new_col2'] = math.nan
df['new_col3'] = df['MSFT']
df['new_col3'] = df['MSFT'].apply(lambda x: x * 2)

df[df['MSFT'] >= 300]
df[( (df['MSFT'] >= 290) & df['MSFT'] <=310 )]

for col in df.columns:
    print(col, df[col].max(), df[col].min(), df[col].mean())


print(df.loc[2:5], '\n', df.iloc[2:5])
print(df.loc[2, 'MSFT'], df['MSFT'].loc[2], '\n', df.iloc[2,0])
print(df.loc[1], '\n', df.iloc[1])


for i in range(0, len(df)):
    df['MSFT'].loc[i]


def get_df_tickers(input_df):
    colnames = []
    for colname in input_df.columns:
        if colname != 'Date':
            colnames.append(colname)
    return colnames

get_df_tickers(df)


# Plotting, matplotlib, Plotly
import matplotlib.pyplot as plt

plt.plot(df['Date'], df['MSFT'])
plt.plot(df['Date'], df['MSFT'].apply(lambda x: x* 0))
plt.plot(df['Date'], df['TSLA'], marker="o")
#plt.show()




import plotly.graph_objects as go
fig = go.Figure()
graph_data = df
for ticker in ['AMZN', 'MSFT', 'TSLA']:
    fig.add_trace(go.Scatter(x=graph_data['Date'], y=graph_data[ticker]
    , name = ticker, mode='lines'))
#fig.show()

