import pandas_datareader
pandas_datareader.__version__
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import plotly.graph_objects as go


import plotly.express as px
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import stocks_data_load
# Load Data

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



available_stocks = get_ticker_names(initial_stocks)


final_stocks_data = pd.read_csv('mystocks.csv')

investment_labels_pie = get_ticker_names(initial_stocks)
investment_amount_pie= np.array(final_stocks_data[get_ticker_headers(initial_stocks, '_initial_total')].tail(1).iloc[0])
current_amount_pie= np.array(final_stocks_data[get_ticker_headers(initial_stocks, '_current_total')].tail(1).iloc[0])

figP = px.pie(values=investment_amount_pie, names=investment_labels_pie)
figP.update_traces(textposition='inside', textinfo='percent+label')
figP.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',
                font=dict(family="Lato", size=14),
                title={
                    'text': "Invested Amount",
                    'x':0.4,
                    'xanchor': 'center',
                    'yanchor': 'top'}, )

figP2 = px.pie(values=current_amount_pie, names=investment_labels_pie)
figP2.update_traces(textposition='inside', textinfo='percent+label')
figP2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',
                font=dict(family="Lato", size=14),
                title={
                    'text': "Current Value",
                    'x':0.4,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                   )




load_figure_template("flatly")
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


all_stocks_dropdown = dcc.Dropdown(id='stock_name'
        , options=[{'label': i, 'value': i} for i in available_stocks], value='AMZN', clearable=False
                                  )

amount_type_drop = dcc.Dropdown(
    id="amount_nominal_percent",
    options=[{"label": i, "value": i} for i in ['Nominal', 'Percent']],
    value="Nominal",
    clearable=False,
    className = 'text-dark',
)

amount_type_drop2 = dcc.Dropdown(
    id="amount_current_initial",
    options=[{"label": i, "value": i} for i in ['Current Value', 'Initial Investment']],
    value="Current Value",
    clearable=False,
    className = 'text-dark',
)


amount_type_drop3 = dcc.Dropdown(
    id="total_amount_current_initial",
    options=[{"label": i, "value": i} for i in ['Current', 'Initial']],
    value="Current",
    clearable=False,
    className = 'text-dark',
)

amount_type_drop4 = dcc.Dropdown(
    id="total_amount_nominal_percent",
    options=[{"label": i, "value": i} for i in ['Nominal', 'Percent']],
    value="Nominal",
    clearable=False,
    className = 'text-dark',
)


tickers = dbc.Checklist(
        id="ticker_checklist",
        options=[
             {"label": "{}".format(i), "value": i}
            for i in available_stocks
        ],
        value=['MSFT', 'NNDM', 'U'],
        switch=True,
        inline = True,
    ),




row = html.Div(
    [
        dbc.Row(
            [dbc.Col([dbc.Label("Select the stocks", className = 'text-dark'),
                      html.Hr(),
                dbc.Row([
                    dbc.Col(tickers)
                ]),]),
                dbc.Col([dcc.Graph(id="single_stock"), dbc.Label('Select the type of profit', className = 'text-dark',), amount_type_drop], width = 5),
                dbc.Col([dcc.Graph(id="single_stock2"), dbc.Label('Select the type of the amount', className = 'text-dark',), amount_type_drop2], width = 5),
            ]
        ),
    ], style = {'padding':'20px 0px 80px 0px'}
)

row2 = html.Div(
    [
        #html.H2("Portion of stock among the totals", className="bg-primary text-white"),
        #html.Hr(),
        
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="total_amounts_plot1"), dbc.Label('Select the type of amount'), amount_type_drop3], width = 6),
                dbc.Col([dcc.Graph(id="total_amounts_plot2"), dbc.Label('Select the type of the profit'), amount_type_drop4], width = 6),
            ]
        ),
    ], style = {'padding':'20px 0px 80px 0px'}
)


row3 = html.Div(
    [
        #html.H2("Portion of stock among the totals", className="bg-primary text-white"),
        #html.Hr(),
        
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="total_values_pie",  figure = figP)], width = 6),
                dbc.Col([dcc.Graph(id="total_values_pie2", figure = figP2)], width = 6),
            ]
        ),
    ], style = {'padding':'20px 0px 80px 0px'}
)


def serve_layout(): 
    return dbc.Container([
    #navbar,
    #html.Hr(),
    html.H2("Performance and comparison of single stocks owned"
            , className="bg-dark text-white text-center p-3"),
    
    dbc.Container([
        dcc.Input(id="input1", type="text", placeholder="", debounce=True),
        html.Div(id="output"),
        row,
        html.Hr(),
    ], fluid=True, className = "border border-top-0 border-dark rounded-bottom"),
    
    html.Br(),
    html.H2("Summary of results of all stocks together"
            , className="bg-dark text-white text-center p-3 rounded-top"),
    
    dbc.Container([
        row2, 
        html.Hr()
    ], fluid=True, className = "border border-top-0 border-dark rounded-bottom"),
    
    html.Br(),
    html.H2("Share of stocks"
            , className="bg-dark text-white text-center p-3 rounded-top"),
    
    dbc.Container([
        row3,
        html.Hr(),
    ], fluid=True, className = "border border-top-0 border-dark rounded-bottom"),
    
    html.Hr(),

], fluid=True)

app.title = "Stocks by T.G."

app.layout = serve_layout()

@app.callback(
    Output("output", "children"),
    Output("input1", "value"),
    Input("input1", "value")
)
def update_output(input1):
    return input1, ''
    

@app.callback(
    Output('single_stock', 'figure'),
    [Input('ticker_checklist', 'value'),
     Input('amount_nominal_percent', 'value')])

def update_graph(_tickers1, _amount_type):
    if _amount_type == 'Nominal':
        column_suffix = '_profit_nominal'
    else:
        column_suffix = '_profit_rate'
 

    fig = go.Figure()
    
    for loop_ticker in _tickers1:
        fig.add_trace(go.Scatter(x=final_stocks_data['Date']
                                 , y=final_stocks_data[loop_ticker + column_suffix]
                            , name=loop_ticker))
    fig.update_layout(
    title={
            'text': "Comparison of single stock profits over time",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
    yaxis_title="Nominal profit amount (USD)" if _amount_type == 'Nominal' else "Profit Percentage",
    font=dict(family="Lato", size=13))
    fig.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig



@app.callback(
    Output('single_stock2', 'figure'),
    [Input('ticker_checklist', 'value'),
     Input('amount_current_initial', 'value')])

def update_graph2(_tickers1, _amount_type2):
    if _amount_type2 == 'Current Value':
        column_suffix = '_current_total'
    else:
        column_suffix = '_initial_total'
        
    fig = go.Figure()
    
    for loop_ticker in _tickers1:
        fig.add_trace(go.Scatter(x=final_stocks_data['Date']
                                 , y=final_stocks_data[loop_ticker + column_suffix]
                            , name=loop_ticker, mode='lines', fill='tozeroy'))
    
    fig.update_layout(
        title={
            'text': "Comparison of single stock values over time",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Current Value (USD)" if _amount_type2 == 'Current Value' else "Invested Amount",
        font=dict(family="Lato", size=13)
    )
    fig.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig


@app.callback(
    Output('total_amounts_plot1', 'figure'),
    [Input('total_amount_current_initial', 'value')])

def update_graph3(_amount_type):
    if _amount_type=='Current':
        col = 'current_value_for_date'
        plotname = 'Total current value of the stocks'
    else:
        col = 'initial_value_for_date'
        plotname = 'Total initial investment value of the stocks'
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=final_stocks_data['Date'], y=final_stocks_data[col]
                            , name='Total current value of stocks', mode='lines', fill='tozeroy'
                              ))
    
    
    
    fig2.update_layout(xaxis_title="Date", yaxis_title="Amount (USD)",
        font=dict(family="Lato", size=14),
        title={
            'text': "Total amount of stocks over time",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        )
    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig2

@app.callback(
    Output('total_amounts_plot2', 'figure'),
    [Input('total_amount_nominal_percent', 'value')])

def update_graph4(_amount_type):
    if _amount_type=='Percent':
        col = 'profit_rate_for_date'
        plotname = 'Total % of profit of all the stocks'
    else:
        col = 'profit_nominal_for_date'
        plotname = 'Total amount of profit of all the stocks'
    fig2 = go.Figure()
    
    pos_data = final_stocks_data[final_stocks_data[col]>=0]
    neg_data = final_stocks_data[final_stocks_data[col]<0]
    
    fig2.add_trace(go.Bar(x=pos_data['Date'], y=pos_data[col]
                            ,  #mode='bar', fill='tozeroy', 
                          marker_color='#18bc9c'
                              ))
    fig2.add_trace(go.Bar(x=neg_data['Date'], y=neg_data[col]
                            , #mode='bar', fill='tozeroy', 
                              marker_color='#e74c3c'
                              ))
    
    fig2.update_layout(xaxis_title="Date", yaxis_title="Amount (USD)" if _amount_type !='Percent' else 'Percent %',
        font=dict(family="Lato", size=14),
        title={
            'text': "Total profit of stocks over time",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
    )
    fig2.update_layout(showlegend=False)
    
    return fig2

app.run_server(debug=False, host='0.0.0.0', port = 80)