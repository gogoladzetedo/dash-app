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


available_stocks = get_ticker_names(initial_stocks)


final_stocks_data = pd.read_csv('mystocks.csv')

investment_labels_pie = get_ticker_names(initial_stocks)
investment_amount_pie= np.array(final_stocks_data[get_ticker_headers(initial_stocks, '_open_initial_value')].tail(1).iloc[0])
current_amount_pie= np.array(final_stocks_data[get_ticker_headers(initial_stocks, '_open_closing_value')].tail(1).iloc[0])

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
        , options=[{'label': i, 'value': i} for i in available_stocks], value='BABA', clearable=False
                                  )

amount_type_drop = dcc.Dropdown(
    id="amount_nominal_percent",
    options=[{"label": i, "value": i} for i in ['Nominal', 'Percent']],
    value="Nominal",
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
        value=['SNOW', 'BABA'],
        switch=True,
        inline = True,
    )


position_types = dcc.Dropdown(
    id="position_types_option_list",
    options=[{"label": i, "value": i} for i in ['open', 'closed', 'both']],
    value="open",
    clearable=False,
    className = 'text-dark',
)

tickers_option = dcc.Dropdown(
    id="tickers_option_list",
    options=[{"label": i, "value": i} for i in available_stocks],
    value="SNOW",
    clearable=False,
    className = 'text-dark',
)


card_content_tickers = [
    dbc.CardHeader("Stocks"),
    dbc.CardBody(
        [
            html.P(
                "Choose the stock names for which you want to display the chart",
                className="card-text",
            ),
            tickers
        ]
    ),
]


card_content_position_types = [
    dbc.CardHeader("Position type"),
    dbc.CardBody(
        [
            
            html.P(
                "Choose the type of positions: closed positions, open positions, or both.",
                className="card-text",
            ),
            position_types
        ]
    ),
]

card_content_amount_type = [
    dbc.CardHeader("Amount Type"),
    dbc.CardBody(
        [
            
            html.P(
                "Choose the type of amount: nominal profit, or a percentage of profit",
                className="card-text",
            ),
            amount_type_drop
        ]
    ),
]

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                    dbc.Row([
                        dbc.Col(dbc.Card(card_content_tickers, color="light", inverse=False))
                        ]
                        , className = "p-1"),
   
                    dbc.Row([
                        dbc.Col(dbc.Card(card_content_position_types, color="light", inverse=False))
                        ]
                        , className = "p-1"),
                    
                    dbc.Row([
                        dbc.Col(dbc.Card(card_content_amount_type, color="light", inverse=False))
                        ]
                        , className = "p-1")
                    ]
                ),
                dbc.Col([dcc.Graph(id="single_stock")], width = 8),
                ]
        ),
    ]
)



row1 = html.Div(
    [
        dbc.Row(
            [dbc.Col([dbc.Label("Select the stock", className = 'text-dark'),
                      html.Hr(),
                dbc.Row([
                    dbc.Col(tickers_option)
                ]),]),
                dbc.Col([dcc.Graph(id="single_stock2")], width = 10),
            ]
        ),
    ]
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


app.title = "Stocks by T.G."
app.layout = dbc.Container([
    
    #navbar,
    #html.Hr(),
    # Chart 1
    html.H2("Comparison of stock profits over time"
            , className="bg-dark text-white text-center p-3"),
    
    dbc.Container([
        row,
        html.Hr(),
    ], fluid=True, className = "p-1"),


    # Chart 2
    html.H2("Performance of stock over time - Initial investment value vs Current value"
            , className="bg-dark text-white text-center p-3"),
    
    dbc.Container([
        row1,
        html.Hr(),
    ], fluid=True, className = "p-1"),


    
    html.Br(),
    html.H2("Summary of results of all stocks together"
            , className="bg-dark text-white text-center p-3 rounded-top"),
    
    dbc.Container([
        row2, 
        html.Hr()
    ], fluid=True, className = "p-1"),
    
    html.Br(),
    html.H2("Share of stocks"
            , className="bg-dark text-white text-center p-3 rounded-top"),
    
    dbc.Container([
        row3,
        html.Hr(),
    ], fluid=True, className = "p-1"),
    
    html.Hr(),
    
], fluid=True, className = "container-md")


# Chart 1 - update by selecting stock tickers and choosing Nominal/Percent   
@app.callback(
    Output('single_stock', 'figure'),
    [Input('ticker_checklist', 'value'),
     Input('amount_nominal_percent', 'value'),
     Input('position_types_option_list', 'value')
     ])

def update_graph(_tickers1, _amount_type, _position_type):
    if _amount_type == 'Nominal':
        column_suffix = '_open_profit_nominal'
    else:
        column_suffix = '_open_profit_rate'
        
 

    fig = go.Figure()
    
    for loop_ticker in _tickers1:
        fig.add_trace(go.Scatter(x=final_stocks_data['Date']
                                 , y=final_stocks_data[loop_ticker + column_suffix]
                            , name=loop_ticker))
    fig.update_layout(
    title={
            'text': "Comparison of profits from active stocks over time",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
    yaxis_title="Nominal profit amount (USD)" if _amount_type == 'Nominal' else "Profit Percentage",
    font=dict(family="Lato", size=13))
    fig.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig


# Chart 2 - update by selecting stock tickers and choosing Initial investment/Current Price

@app.callback(
    Output('single_stock2', 'figure'),
    Input('tickers_option_list', 'value'))

def update_graph2(_ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=final_stocks_data['Date']
                                 , y=final_stocks_data[_ticker + '_open_closing_value']
                            , name= 'Current value', mode='lines', fill='tozeroy'))
    fig.add_trace(go.Scatter(x=final_stocks_data['Date']
                                 , y=final_stocks_data[_ticker + '_open_initial_value']
                            , name='Initial investment value', mode='lines', fill='tozeroy'))
    
    fig.update_layout(
        title={
            'text': "Comparison of single stock values over time",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Current Value and Initial investment value (USD)",
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
        col = 'open_closing_value_for_date'
        plotname = 'Total current value of the stocks'
    else:
        col = 'open_initial_value_for_date'
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
        col = 'open_profit_rate_for_date'
        plotname = 'Total % of profit of all the stocks'
    else:
        col = 'open_profit_nominal_for_date'
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