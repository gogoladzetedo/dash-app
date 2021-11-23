from dash import Dash
import plotly.express as px
from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import data.data_functions
import interface_helpers.layout as ifc

def tickers_checklist(component_id):
    return dbc.Checklist(
        id=component_id,
        options=[{"label": "{}".format(i), "value": i} for i in ifc.available_stocks()],
        #value=['SNOW', 'BABA'],
        switch=True,
        inline = True
    )

def tickers_option(component_id):
    return dcc.Dropdown(
        id=component_id,
        options=[{"label": i, "value": i} for i in ifc.available_stocks()],
        #value="SNOW",
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

def profit_or_amount_option(component_id):
    return dcc.Dropdown(
        id=component_id,
        options=[{"label": i, "value": i} for i in ['Profits', 'Investments']],
        value="Investments",
        clearable=False,
        className = 'text-dark',
    )

### CARDS HERE ###

def card_ticker_checklist(component):
    return [
        dbc.CardBody([
            html.H5("Stocks", className="card-title"),
            html.P(
                "Choose the stock names for which you want to display the chart:",
                className="card-text",
            ),
            tickers_checklist(component)
        ])
    ]

def card_position_types(component):
    return [
        dbc.CardBody([
            html.H5("Past and Present", className="card-title"),
            html.P("Choose type of positions: closed positions, open, or both.:", className="card-text"),
            position_types(component)
        ]),
    ]

def card_amount_type(component):
    return [
        dbc.CardBody([
            html.H5("Amount / Rate", className="card-title"),
            html.P("Choose the type of amount to show: nominal, or a percentage:", className="card-text"),
            amount_type_drop(component)
        ]),
    ]

def card_position_value_type(component):
    return [
        dbc.CardBody([
            html.H5("Investment Value", className="card-title"),
            html.P("Choose the type of value of positions: Initial investment value, or a current/closing value:"
                ,className="card-text"),
            position_value_type(component)
        ]),
    ]

def card_ticker_options(component):
    return [
        dbc.CardBody([
            html.H5("Stock", className="card-title"),
            html.P("Select the stock names for which you want to see the chart:", className="card-text"),
            tickers_option(component)
        ]),
    ]

def card_profit_or_amount_option(component):
    return [
        dbc.CardBody([
            html.H5("Profit / Investment", className="card-title"),
            html.P("Select the metric to output on the graph:", className="card-text"),
            profit_or_amount_option(component)
        ]),
    ]


def empty_card(title):
    return [
        dbc.CardHeader(title),
        dbc.CardBody([]),
    ]

def graph_card(component_id):
    return [dbc.CardBody([dcc.Graph(id=component_id)])]


def card_input_submit():
    return [
        dbc.CardBody([
            dbc.Col(html.Button('Load data and calculate', id='data-load', n_clicks=0
            , className = 'btn btn-success m-1 disabled', disabled=True)),
            dbc.Col(html.Div(id='load-output-area', children='Click "Load and Calculate" once you are done with entering oeprations.'
            , className = 'text-dark m-1')),
            dbc.Col(html.Div(id='load-output-area2')),
        ])
    ]

def card_input_data():
    return [
        dbc.CardBody([
            html.H5("Manual Input", className="card-title"),
            html.P("Add the details of each trade operation separately. For sell operations add minus sign before quantity."
            , className="card-text"),
            html.P("After adding the details of a single transaction, click 'Add Operation' button and start entering the next oepration."
            , className="card-text"),
            dbc.Col(dcc.Input(id='stock-name', type='text', placeholder = 'Name of stock ticker'
            , className = 'text-dark form-control m-1')),
            dbc.Col(dcc.Input(id='stock-buy-date', type='text', placeholder = 'Date of the operation in YYYY-MM-DD format.'
            , className = 'text-dark form-control m-1')),
            dbc.Col(dcc.Input(id='stock-price', type='number', placeholder = 'Price of single stock'
            , className = 'text-dark form-control m-1')),
            dbc.Col(dcc.Input(id='stock-amount', type='number', placeholder = 'Number of stock'
            , className = 'text-dark form-control m-1')),
            dbc.Col(html.Button('Add operation', id='submit-val', n_clicks=0
            , className = 'btn btn-info m-1')),
            dbc.Col(html.Pre(id='container-button-basic', children='Enter values and press "Add" button '
            , className = 'text-dark m-1')),
        ])
    ]

def card_upload_file():
    return [
        dbc.CardBody([
            html.H5("File Upload", className="card-title"),
            html.Div([
                html.P("Upload a .csv file containing the portfolio operations, each operation ona separate line."+
                " File must not contain header. Order of columns is respective to the manual input:"),
                html.Ul([
                    html.Li(["Stock ticker name", html.Ul(html.Li("Example: MSFT"), className = "font-italic")]),
                    html.Li(["Operation date in YYYY-MM-DD format", html.Ul(html.Li("Example: 2021-03-25"), className = "font-italic")]),
                    html.Li(["Price of single unit of stock", html.Ul(html.Li("Example: 290"), className = "font-italic")]),
                    html.Li(["Quantity of the purchased stocks. If it's a sell oepration, add a minus before."
                    , html.Ul([html.Li("Example for purchase: 10"), html.Li("Example for Sell: -10")], className = "font-italic")]),]
                ),
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(["Drag and Drop or Select a File"]),
                    multiple=False,
                    style={
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "1px",
                        "borderColor": "black"
                    },
                    className = "form-control btn btn-info",
                ),
                dbc.Label(id="upload-data-text", className="form-label", children="upload .csv file below"),]
                , className="form-group", id="form_for_file_upload"
            ),
        ])
    ]

