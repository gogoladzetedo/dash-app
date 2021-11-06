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



row1 = html.Div(
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

row2 = html.Div([
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

row3 = html.Div([
    dbc.Row([

        dbc.Col([
            
            
            dbc.Row([
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
            , dbc.Row([
                dbc.Col([
                    dbc.Col(dbc.Card(crd.graph_card('total_amounts_plot2') , className="shadow-sm"))
                    ])
                ], className = "p-1")
        ]
            , width = 8
        )
    ]),
])

row4 = html.Div([
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



tabs = dbc.Tabs(
    [
        dbc.Tab(row1, tab_id="row1", label="Stock profits comparison"),
        dbc.Tab(row2, tab_id="row2", label="Performance of a single stock"),
        dbc.Tab(row3, tab_id="row3", label="Summary of the whole portfolio"),
        dbc.Tab(row4, tab_id="row4", label="Share of stocks"),
    ],
    id="tabs",
    active_tab="row1"
)