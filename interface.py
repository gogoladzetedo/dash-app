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


available_stocks = d_f.get_ticker_names(d_f.initial_stocks)
final_stocks_data_last_rec = d_f.input_file('mystocks.csv').tail(1).copy()



row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                    dbc.Row([
                        dbc.Col(dbc.Card(crd.card_ticker_checklist('ticker_checklist') , color="light", outline=False))
                        ]
                        , className = "p-1"),
   
                    dbc.Row([
                        dbc.Col(dbc.Card(crd.card_position_types('position_types_option_list')
                        , color="light", outline=False))
                        ]
                        , className = "p-1"),
                    
                    dbc.Row([
                        dbc.Col(dbc.Card(crd.card_amount_type('amount_nominal_percent') , color="light", outline=False))
                        ]
                        , className = "p-1")
                    ]
                ),
                dbc.Col(
                    dbc.Row([
                        dbc.Col([
                            dbc.Card(crd.empty_card('Profits over time') , color="light", outline=True),
                            dcc.Graph(id="single_stock")
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

row1 = html.Div([
    dbc.Row([

        dbc.Col([

            dbc.Row([
                dbc.Col(dbc.Card(crd.card_ticker_options('tickers_option_list') , color="light", outline=False))
                ], className = "p-1"
            ),

            dbc.Row([
                dbc.Col(dbc.Card(
                    crd.card_position_types('position_types_option_list_2'), 
                    color="light", outline=False))
                ], className = "p-1"
            ),
            
        ]),
        dbc.Col(
            dbc.Row([
                dbc.Col([
                    dbc.Card(crd.empty_card('Position value over time') , color="light", outline=True),
                    dcc.Graph(id="single_stock2")
                    ])
                ]
                , className = "p-1"
            )
            , width = 8
        ),
    ]),
])

row2 = html.Div([
    dbc.Row([

        dbc.Col([

            dbc.Row([
                dbc.Col(dbc.Card(crd.card_position_types('position_types_option_list_3') , color="light", outline=False))
                ], className = "p-1"
            ),

            dbc.Row([
                dbc.Col(dbc.Card(
                    crd.card_amount_type('amount_nominal_percent_2'), 
                    color="light", outline=False))
                ], className = "p-1"
            ),
            
        ]),
        dbc.Col(
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="total_amounts_plot1"),
                    dcc.Graph(id="total_amounts_plot2")
                    ])
                ]
                , className = "p-1"
            )
            , width = 9
        ),
    ]),
])

row3 = html.Div([
    dbc.Row([

        dbc.Col([

            dbc.Row([
                dbc.Col(dbc.Card(crd.card_position_types('position_types_option_list_4') , color="light", outline=False))
                ], className = "p-1"
            ),

            dbc.Row([
                dbc.Col(dbc.Card(
                    crd.card_position_value_type('position_value_types_option_list'), 
                    color="light", outline=False))
                ], className = "p-1"
            ),
            
        ]),
        dbc.Col(
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="total_values_pie")
                    ])
                ]
                , className = "p-1"
            )
            , width = 9
        ),
    ]),    
])