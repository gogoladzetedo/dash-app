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
import data.stocks_data_load

# local functions
import data.data_functions as d_f
import interface_helpers.cards as crd


def available_stocks():
    return d_f.get_ticker_names(d_f.initial_stocks())
def final_stocks_data_last_rec():
    return d_f.input_file('data/mystocks.csv').tail(1)



def row1():
     return html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                    dbc.Row([
                        dbc.Col(dbc.Card(crd.card_ticker_checklist('ticker_checklist') , className="shadow-sm"))
                        ]
                        , className = "p-1"),
   
                    dbc.Row([
                        dbc.Col(dbc.Card(crd.card_position_types('position_types_option_list'),  className="shadow-sm"))
                        ]
                        , className = "p-1"),
                    
                    dbc.Row([
                        dbc.Col(dbc.Card(crd.card_amount_type('amount_nominal_percent') , className="shadow-sm"))
                        ]
                        , className = "p-1")
                    ]
                ),
                dbc.Col(
                    dbc.Row([
                        dbc.Col([
                            dbc.Col(dbc.Card(crd.graph_card('single_stock') , className="shadow-sm"))
                            ])
                        ]
                        , className = "p-1"
                    )
                    , width = 8
                ),
            ]
        ),
    ]
)

def row2():
    return html.Div([
    dbc.Row([

        dbc.Col([

            dbc.Row([
                dbc.Col(dbc.Card(crd.card_ticker_options('tickers_option_list'), className="shadow-sm"))
                ], className = "p-1"
            ),

            dbc.Row([
                dbc.Col(dbc.Card(
                    crd.card_position_types('position_types_option_list_2'), className="shadow-sm"))
                ], className = "p-1"
            ),
            
        ]),
        dbc.Col(
            dbc.Row([
                dbc.Col([
                    dbc.Col(dbc.Card(crd.graph_card('single_stock2') , className="shadow-sm"))
                    ])
                ]
                , className = "p-1"
            )
            , width = 8
        ),
    ]),
])

def row3():
    return html.Div([
    dbc.Row([

        dbc.Col([
            
            dbc.Row([
                dbc.Col(dbc.Card(
                    crd.card_profit_or_amount_option('amount_profit_investment'), className="shadow-sm"))
                ], className = "p-1"
            )
            , dbc.Row([
                dbc.Col(dbc.Card(crd.card_position_types('position_types_option_list_3'), className="shadow-sm"))
                ], className = "p-1"
            ) 
            , dbc.Row([
                dbc.Col(dbc.Card(
                    crd.card_amount_type('amount_nominal_percent_2'), className="shadow-sm"))
                ], className = "p-1"
            )
            
            
        ]),
        
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Col(dbc.Card(crd.graph_card('total_amounts_plot1') , className="shadow-sm"))
                    ])
                ], className = "p-1"
                
            )
        ]
            , width = 8
        )
    ]),
])

def row4():
    return html.Div([
    dbc.Row([

        dbc.Col([

            dbc.Row([
                dbc.Col(dbc.Card(crd.card_position_types('position_types_option_list_4'), className="shadow-sm"))
                ], className = "p-1"
            ),

            dbc.Row([
                dbc.Col(dbc.Card(
                    crd.card_position_value_type('position_value_types_option_list'), className="shadow-sm"))
                ], className = "p-1"
            ),
            
        ]),
        dbc.Col(
            dbc.Row([
                dbc.Col([
                    dbc.Col(dbc.Card(crd.graph_card('total_values_pie') , className="shadow-sm"))
                    ])
                ]
                , className = "p-1"
            )
            , width = 8
        ),
    ]),    
])


def row_input():
    return [ dbc.Col(
        dbc.CardBody([
            html.H5("Purchase / Sell", className="card-title"),
            html.P("add the details of each trade operation separately. For sell operations add minus sign before quantity."
            , className="card-text"),
            dbc.Col(dcc.Input(id='stock-name', type='text', placeholder = 'Name of stock ticker'
            , className = 'text-dark form-control m-1')),
            dbc.Col(dcc.Input(id='stock-buy-date', type='text', placeholder = 'Date of the operation in DD-MM-YYYY format.'
            , className = 'text-dark form-control m-1')),
            dbc.Col(dcc.Input(id='stock-price', type='number', placeholder = 'Price of single stock'
            , className = 'text-dark form-control m-1')),
            dbc.Col(dcc.Input(id='stock-amount', type='number', placeholder = 'Number of stock'
            , className = 'text-dark form-control m-1')),
            dbc.Col(html.Button('Add operation', id='submit-val', n_clicks=0
            , className = 'text-dark btn btn-success m-1 border-bottom')),
            dbc.Col(html.Pre(id='container-button-basic', children='Enter values and press "Add" button '
            , className = 'text-dark m-1')),

            dbc.Col(html.Button('Load data and calculate', id='data-load', n_clicks=0
            , className = 'text-dark btn btn-success m-1 border-bottom')),
            dbc.Col(html.Div(id='load-output-area', children='Click "Load and Calculate" once you are done with entering oeprations.'
            , className = 'text-dark m-1')),
            dbc.Col(html.Div(id='load-output-area2')),
        ])
    , className="mt-4")]

def tabs():
    return dbc.Tabs(
    [
        dbc.Tab(row_input(), tab_id="row_input", label="Add portfolio |"),
        dbc.Tab(row1(), tab_id="row1", label="Compare Stock profits |"),
        dbc.Tab(row2(), tab_id="row2", label="Single stock performance |"),
        dbc.Tab(row3(), tab_id="row3", label="Portfolio summary |"),
        dbc.Tab(row4(), tab_id="row4", label="Share of stocks |"),
        
    ],
    id="tabs",
    active_tab="row_input"
)