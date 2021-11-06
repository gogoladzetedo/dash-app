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

# local functions
import data_functions as d_f
import cards as crd
import interface as ifc


available_stocks = d_f.get_ticker_names(d_f.initial_stocks)
final_stocks_data = d_f.input_file('mystocks.csv')


load_figure_template("bootstrap")
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.title = "Stocks by T.G."
app.layout = dbc.Container([
    
    html.H2("Comparison of stock profits over time"
            , className="bg-dark text-white text-center p-3"),
    
    dbc.Container([
        ifc.row,
        html.Hr(),
    ], fluid=True, className = "p-1"),


    # Chart 2
    html.H2("Performance of stock over time - Initial investment value vs Current value"
            , className="bg-dark text-white text-center p-3"),
    
    dbc.Container([
        ifc.row1,
        html.Hr(),
    ], fluid=True, className = "p-1"),


    
    html.Br(),
    html.H2("Summary of results of all stocks together"
            , className="bg-dark text-white text-center p-3 rounded-top"),
    
    dbc.Container([
        ifc.row2, 
        html.Hr()
    ], fluid=True, className = "p-1"),
    
    html.Br(),
    html.H2("Share of stocks"
            , className="bg-dark text-white text-center p-3 rounded-top"),
    
    dbc.Container([
        ifc.row3,
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
    if _position_type == 'open':
        col_suffix_position = '_open'
        graph_title = 'open position stocks'
    elif _position_type == 'closed':
        col_suffix_position = '_closed'
        graph_title = 'closed position stocks'
    else:
        col_suffix_position = '_total'
        graph_title = 'both, open and closed position stocks'

    col_suffix_metric = '_profit'

    if _amount_type == 'Nominal':
        col_suffix_amount = '_nominal'
    else:
        col_suffix_amount = '_rate'
    
    fig = go.Figure()
    
    for loop_ticker in _tickers1:
        fig.add_trace(go.Scatter(x=final_stocks_data['Date']
                                 , y=final_stocks_data[loop_ticker + col_suffix_position + col_suffix_metric + col_suffix_amount]
                            , name=loop_ticker))
    fig.update_layout(
        template = 'plotly_white',
        title={
                'text': 'Comparison of profits from ' + graph_title + ' over time',
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
        yaxis_title="Nominal profit amount (USD)" if _amount_type == 'Nominal' else "Profit Percentage",
        font=dict(family="Lato", size=13)
    )
    fig.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig

@app.callback(
    Output('single_stock2', 'figure'),
    [Input('tickers_option_list', 'value'),
     Input('position_types_option_list_2', 'value')
    ])

def update_graph2(_ticker, _position_type):
    if _position_type == 'open':
        col_suffix_position = '_open'
        graph_title = 'open position stock'
    elif _position_type == 'closed':
        col_suffix_position = '_closed'
        graph_title = 'closed position stock'
    else:
        col_suffix_position = '_total'
        graph_title = 'both, open and closed position stock'

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=final_stocks_data['Date']
                                 , y=final_stocks_data[_ticker + col_suffix_position + '_closing_value']
                            , name= 'Closing value', mode='lines', fill='tozeroy', marker_color='#18bc9c'))
    fig.add_trace(go.Scatter(x=final_stocks_data['Date']
                                 , y=final_stocks_data[_ticker + col_suffix_position + '_initial_value']
                            , name='Initial investment value', mode='lines', fill='tozeroy', marker_color='#e74c3c'))
    
    fig.update_layout(
        template = 'plotly_white',
        title={
            'text': 'Comparison of ' + graph_title + ' values over time',
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Closing Value and Initial investment value (USD)",
        font=dict(family="Lato", size=13)
    )
    fig.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig

@app.callback(
    Output('total_amounts_plot1', 'figure'),
    Input('position_types_option_list_3', 'value'))

def update_graph3(_position_type):
    if _position_type == 'open':
        col_suffix_position = 'open'
        graph_title = 'open position stocks'
    elif _position_type == 'closed':
        col_suffix_position = 'closed'
        graph_title = 'closed position stocks'
    else:
        col_suffix_position = 'total'
        graph_title = 'both, open and closed position stocks'

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=final_stocks_data['Date'], y=final_stocks_data[col_suffix_position + '_closing_value_for_date']
                            , name='Closing/current value', mode='lines', fill='tozeroy', marker_color='#18bc9c'
                              ))

    fig2.add_trace(go.Scatter(x=final_stocks_data['Date'], y=final_stocks_data[col_suffix_position + '_initial_value_for_date']
                            , name='Initial investment', mode='lines', fill='tozeroy', marker_color='#e74c3c'
                              ))
    fig2.update_layout(
        template = 'plotly_white',
        xaxis_title="Date", yaxis_title="Amount (USD)",
        font=dict(family="Lato", size=14),
        title={
            'text': 'Total amount of ' + graph_title + ' over time',
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        )
    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig2


@app.callback(
    Output('total_amounts_plot2', 'figure'),
    [Input('amount_nominal_percent_2', 'value'),
     Input('position_types_option_list_3', 'value')])

def update_graph4(_amount_type, _position_type):
    if _position_type == 'open':
        col_suffix_position = 'open'
        graph_title = 'open position stocks'
    elif _position_type == 'closed':
        col_suffix_position = 'closed'
        graph_title = 'closed position stocks'
    else:
        col_suffix_position = 'total'
        graph_title = 'both, open and closed position stocks'

    col_suffix_metric = '_profit'

    if _amount_type == 'Nominal':
        col_suffix_amount = '_nominal'
    else:
        col_suffix_amount = '_rate'

    col = col_suffix_position + col_suffix_metric + col_suffix_amount + '_for_date'
   
    fig2 = go.Figure()
    pos_data = final_stocks_data[final_stocks_data[col]>=0]
    neg_data = final_stocks_data[final_stocks_data[col]<0]
    
    fig2.add_trace(go.Bar(x=pos_data['Date'], y=pos_data[col]
                            ,  #mode='bar', fill='tozeroy', 
                          marker_color='#18bc9c', name = 'Total profit'
                              ))
    fig2.add_trace(go.Bar(x=neg_data['Date'], y=neg_data[col]
                            , #mode='bar', fill='tozeroy', 
                              marker_color='#e74c3c', name = 'Total loss'
                              ))
    fig2.update_layout(
        template = 'plotly_white',
        xaxis_title="Date", yaxis_title="Amount (USD)" if _amount_type !='Percent' else 'Percent %',
        font=dict(family="Lato", size=14),
        title={
            'text': 'Total profit of ' + graph_title + 'stocks over time',
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
    )
    fig2.update_layout(showlegend=False)
    
    return fig2


@app.callback(
    Output('total_values_pie', 'figure'),
    [Input('position_types_option_list_4', 'value'),
     Input('position_value_types_option_list', 'value')])

def update_graph5(_position_type, _position_value_type):
    if _position_type == 'open':
        col_suffix_position = '_open'
        graph_title = 'open position stocks'
    elif _position_type == 'closed':
        col_suffix_position = '_closed'
        graph_title = 'closed position stocks'
    else:
        col_suffix_position = '_total'
        graph_title = 'both, open and closed position stocks'


    if _position_value_type == 'Invested Value':
        col_suffix_value = '_initial_value'
        graph_title = graph_title + ', initially invested value'
    else:
        col_suffix_value = '_closing_value'
        graph_title = graph_title + ', current/closing value'

    cols = d_f.get_ticker_headers(d_f.initial_stocks, (col_suffix_position + col_suffix_value))
   
    investment_labels_pie = d_f.get_ticker_names(d_f.initial_stocks)
    investment_amount_pie= np.array(ifc.final_stocks_data_last_rec[cols].iloc[0])
    
    fig = go.Figure()

    fig = px.pie(values=investment_amount_pie, names=investment_labels_pie)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',
                    font=dict(family="Lato", size=14),
                    template = 'plotly_white',
                    title={
                        'text': 'Investment Amounts: ' + graph_title,
                        'x':0.4,
                        'xanchor': 'center',
                        'yanchor': 'top'}, )
    
    return fig


app.run_server(debug=False, host='0.0.0.0', port = 80)