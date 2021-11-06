from dash import Dash
import plotly.express as px
from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import data_functions

available_stocks = data_functions.get_ticker_names(data_functions.initial_stocks)

def tickers_checklist(component_id):
    return dbc.Checklist(
        id=component_id,
        options=[
             {"label": "{}".format(i), "value": i}
            for i in available_stocks
        ],
        value=['SNOW', 'BABA'],
        switch=True,
        inline = True,
    )

def tickers_option(component_id):
    return dcc.Dropdown(
        id=component_id,
        options=[{"label": i, "value": i} for i in available_stocks],
        value="SNOW",
        clearable=False,
        className = 'text-dark',
)

def position_types(component_id):
    return dcc.Dropdown(
        id=component_id,
        options=[{"label": i, "value": i} for i in ['open', 'closed', 'both']],
        value="open",
        clearable=False,
        className = 'text-dark',
        )

def amount_type_drop(component_id):
    return dcc.Dropdown(
        id=component_id,
        options=[{"label": i, "value": i} for i in ['Nominal', 'Percent']],
        value="Nominal",
        clearable=False,
        className = 'text-dark',
    )

def position_value_type(component_id):
    return dcc.Dropdown(
        id=component_id,
        options=[{"label": i, "value": i} for i in ['Invested Value', 'Current/Closing Value']],
        value="Current/Closing Value",
        clearable=False,
        className = 'text-dark',
    )


def card_ticker_checklist(component):
    return [
    dbc.CardHeader("Stocks"),
    dbc.CardBody(
        [
            html.P(
                "Choose the stock names for which you want to display the chart",
                className="card-text",
            ),
            tickers_checklist(component)
        ]
    ),
]

def card_position_types(component):
    return [
            dbc.CardHeader("Position type"),
            dbc.CardBody(
                [
                    html.P(
                        "Choose the type of positions: closed positions, open positions, or both.",
                        className="card-text",
                    ),
                    position_types(component)
                ]
            ),
        ]

def card_amount_type(component):
    return [
        dbc.CardHeader("Amount Type"),
        dbc.CardBody(
            [
                
                html.P(
                    "Choose the type of amount: nominal profit, or a percentage of profit",
                    className="card-text",
                ),
                amount_type_drop(component)
            ]
        ),
    ]

def card_position_value_type(component):
    return [
        dbc.CardHeader("Position value type"),
        dbc.CardBody(
            [
                
                html.P(
                    "Choose the type of value of positions: Initial investment value, or a current/closing value",
                    className="card-text",
                ),
                position_value_type(component)
            ]
        ),
    ]

def card_ticker_options(component):
    return [
    dbc.CardHeader("Stock position"),
    dbc.CardBody(
        [
            
            html.P(
                "Select the stock",
                className="card-text",
            ),
            tickers_option(component)
        ]
    ),
]

def empty_card(title):
    return [
        dbc.CardHeader(title),
        dbc.CardBody([]),
    ]