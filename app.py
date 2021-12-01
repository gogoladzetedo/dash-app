
import pandas_datareader
pandas_datareader.__version__
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.graph_objects as go
import json
import math
import time

import plotly.express as px
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# local functions
import data.data_functions as d_f
import interface_helpers.layout as ifc
import data.stocks_data_load as sdl



available_stocks = ifc.available_stocks()
def final_stocks_data():
    return d_f.input_file('data/mystocks.csv')

# lux was BEST so far.
# materia also OK
# darkly is ok, for dark
# flatly and bootstrap is OK
# sandstone is OK. gray and solid
# sketchy is good but graphs are not matching the style
# slate is ok, DARK
# solar is dark and green. OK
# superhero is dark gray and blue.
# yeti

load_figure_template("lux")
figure_tmeplate = "lux" 
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])


app.title = "Portfolio Analytics"

def serve_layout(): 
    return dbc.Container([ 
        html.H2("Stock Portfolio Dashboard", className="bg-dark text-white text-center p-3"),



        dbc.Modal(
            [
                dbc.ModalHeader("Please wait whle data is calculated..."),
                dbc.ModalBody(
                    dcc.Loading(id="ls-loading-1", children=[html.Div(id="ls-loading-output-1")], type="default"),
                ),
                dbc.ModalFooter(
                ),
            ],
            id="modal",
            is_open=False,
        ),


        

        dbc.Col(ifc.tabs("row_input"), width=12, className="mt-4", id="col-tabs"),
        dbc.Col(html.Br() ),
        dbc.Col(
            html.Footer(
                html.A(children="project repo on GitHub", href='https://github.com/gogoladzetedo/dash-app')
                , className="card-footer text-muted text-center bg-secondary")

        )
    ], fluid=True, className = "container-md")

app.layout = serve_layout()

#@app.callback(
#    Output('row1', 'value'),
#    Input('tabs', 'value')
#)
#def update_tab1(_tab_content):
#    app.layout = serve_layout()
#    return ifc.row1
        

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
        fig.add_trace(go.Scatter(x=final_stocks_data()['Date']
                                 , y=final_stocks_data()[loop_ticker + col_suffix_position + col_suffix_metric + col_suffix_amount]
                            , name=loop_ticker))
    fig.update_layout(
        template = figure_tmeplate,
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
    fig.add_trace(go.Scatter(x=final_stocks_data()['Date']
                                 , y=final_stocks_data()[_ticker + col_suffix_position + '_closing_value']
                            , name= 'Closing value', mode='lines', fill='tozeroy', marker_color='#18bc9c'))
    fig.add_trace(go.Scatter(x=final_stocks_data()['Date']
                                 , y=final_stocks_data()[_ticker + col_suffix_position + '_initial_value']
                            , name='Initial investment value', mode='lines', fill='tozeroy', marker_color='#e74c3c'))
    
    fig.update_layout(
        template = figure_tmeplate,
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
    [Input('position_types_option_list_3', 'value'),
     Input('amount_profit_investment', 'value'),
     Input('amount_nominal_percent_2', 'value')])

def update_graph3(_position_type, _profit_investment, _amount_type):
    # Both graphs
    if _position_type == 'open':
        col_suffix_position = 'open'
        graph_title = 'open position stocks'
    elif _position_type == 'closed':
        col_suffix_position = 'closed'
        graph_title = 'closed position stocks'
    else:
        col_suffix_position = 'total'
        graph_title = 'both, open and closed position stocks'

    ## Only graph 2
    col_suffix_metric = '_profit'

    if _amount_type == 'Nominal':
        col_suffix_amount = '_nominal'
    else:
        col_suffix_amount = '_rate'

    col = col_suffix_position + col_suffix_metric + col_suffix_amount + '_for_date'


    if _profit_investment == 'Investments':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=final_stocks_data()['Date'], y=final_stocks_data()[col_suffix_position + '_closing_value_for_date']
                                , name='Closing/current value', mode='lines', fill='tozeroy', marker_color='#18bc9c'
                                ))

        fig.add_trace(go.Scatter(x=final_stocks_data()['Date'], y=final_stocks_data()[col_suffix_position + '_initial_value_for_date']
                                , name='Initial investment', mode='lines', fill='tozeroy', marker_color='#e74c3c'
                                ))
        fig.update_layout(
            template = figure_tmeplate,
            xaxis_title="Date", yaxis_title="Amount (USD)",
            font=dict(family="Lato", size=14),
            title={
                'text': 'Total amount of ' + graph_title + ' over time',
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            )
        fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
    else:
        fig = go.Figure()
        pos_data = final_stocks_data()[final_stocks_data()[col]>=0]
        neg_data = final_stocks_data()[final_stocks_data()[col]<0]
        
        fig.add_trace(go.Bar(x=pos_data['Date'], y=pos_data[col]
                                ,  #mode='bar', fill='tozeroy', 
                            marker_color='#18bc9c', name = 'Total profit'
                                ))
        fig.add_trace(go.Bar(x=neg_data['Date'], y=neg_data[col]
                                , #mode='bar', fill='tozeroy', 
                                marker_color='#e74c3c', name = 'Total loss'
                                ))
        fig.update_layout(
            template = figure_tmeplate,
            xaxis_title="Date", yaxis_title="Amount (USD)" if _amount_type !='Percent' else 'Percent %',
            font=dict(family="Lato", size=14),
            title={
                'text': 'Total profit of ' + graph_title + ' over time',
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
        )
        fig.update_layout(showlegend=False)

    return fig




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

    cols = d_f.get_ticker_headers(d_f.initial_stocks(), (col_suffix_position + col_suffix_value))
   
    investment_labels_pie = d_f.get_ticker_names(d_f.initial_stocks())
    investment_amount_pie= ifc.final_stocks_data_last_rec()[cols].iloc[0].tolist()
    
    fig = go.Figure()

    fig = px.pie(values=investment_amount_pie, names=investment_labels_pie)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',
                    font=dict(family="Lato", size=14),
                    template = figure_tmeplate,
                    title={
                        'text': graph_title,
                        'x':0.4,
                        'xanchor': 'center',
                        'yanchor': 'top'}, )
    return fig


##### Functionality for the input data #####



all_stocks = {}

@app.callback(
    Output('container-button-basic', 'children'),

    Output('stock-name', 'value'),
    Output('stock-buy-date', 'value'),
    Output('stock-price', 'value'),
    Output('stock-amount', 'value'),

    #Output('data-load', 'className'),
    #Output('data-load', 'disabled'),

    Input('submit-val', 'n_clicks'),
    State('stock-name', 'value'),
    State('stock-buy-date', 'value'),
    State('stock-price', 'value'),
    State('stock-amount', 'value'),
    State('container-button-basic', 'children')
)
def update_output(n_clicks, name, date, price, amount, text):
    if (name is not None 
        and date is not None
        and price is not None
        and amount is not None 
        and n_clicks > 0):
        
        current_stock = {}
        current_stock['price'] = price
        current_stock['quantity'] = amount
        if price is None:
            price = 0
        if amount is None:
            amount = 0
        current_stock['value'] = price * amount
        current_stock['date'] = date
        current_stock['is_empty'] = 0

        if name in all_stocks:
            added_current_stock = all_stocks[name].copy()
            added_current_stock.append(current_stock)
        else:
            added_current_stock = []
            added_current_stock.append(current_stock)
        all_stocks[name] = added_current_stock

        if amount < 0:
            oprtation_type='Sold'
        else:  
            oprtation_type='Purchased'

        current_operations_txt = '- ' + oprtation_type + ' {} items of "{}" stock, on {} each priced as {}'.format(
            amount, name, date, price, n_clicks)
        text = text + '\n' + current_operations_txt

        with open('data/initial_positions.json', 'w') as fp:
            json.dump(all_stocks, fp, sort_keys=True, indent=4)
        
        classN = "btn btn-success m-1"
        is_disabled = False
    else:
        classN = "btn btn-success m-1 disabled"
        is_disabled = True

    return text, '', '', math.nan, math.nan#, classN, is_disabled



@app.callback(
    Output('upload-data-text', 'children'),
    #Output('data-load', 'className'),
    #Output('data-load', 'disabled')
     
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename')]
)
def updload_file(_contents, _filename):    
    if _contents:
        try:
            df = d_f.parse_contents(_contents, _filename)
            df = d_f.rename_df_columns(df)
            _all_stocks = d_f.df_to_dict(df)
            with open('data/initial_positions.json', 'w') as fp:
                json.dump(_all_stocks, fp, sort_keys=True, indent=4)
            res = html.P('File upload Completed! Click "Load and Calculate" to calculate dashboard metrics'
            , className="font-weight-bold text-success")
            #classN = "btn btn-success m-1"
            #is_disabled = False
        except Exception as e:
            print(e)
            res = html.P('Upload process failed! Please, check file requirements listed above.'
            , className="font-weight-bold text-danger")
            #classN = "btn btn-success m-1 disabled"
            #is_disabled = True

    else:
        res = 'upload .csv file below' 
        #classN = "btn btn-success m-1 disabled"
        #is_disabled = True
    return res #, classN, is_disabled



        

@app.callback(
    [Output('load-output-area', 'children'),
    Output('load-output-area2', 'children'),
    Output('col-tabs', 'children')],
    Input('data-load', 'n_clicks'),
)
def calcualte_data(n_clicks):
    if n_clicks > 0:
        
        sdl.run_data_load(d_f.initial_stocks())
        res = html.P('Calculation complete! Check the metrics.'
            , className="font-weight-bold text-success")

        return 'Data Load has been Completed!', res, ifc.tabs("row1")

@app.callback(Output("ls-loading-output-1", "children"), Input("data-load", "n_clicks"))
def input_triggers_spinner(n_clicks):
    if n_clicks > 0:
        time.sleep(15)
        return ''

@app.callback(Output("modal", "is_open"), Input("data-load", "n_clicks"))
def input_triggers_modal(n_clicks):
    if n_clicks > 0:
        return True




app.run_server(debug=False, host='0.0.0.0', port = 80)