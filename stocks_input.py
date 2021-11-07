from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import json

# load local libraries
import stocks_data_load as sdl
import interface as ifc
import cards as crd

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

def serve_layout(): 
    return dbc.Container([ 
        html.H2("Add Your Portfolio", className="bg-dark text-white text-center p-3"),
        dbc.Col(crd.card_input_data()
            , className="mt-4"),
    ], fluid=True, className = "container-md")
    
    

app.layout = serve_layout()

all_stocks = {}

@app.callback(
    Output('container-button-basic', 'children'),

    Output('stock-name', 'value'),
    Output('stock-buy-date', 'value'),
    Output('stock-price', 'value'),
    Output('stock-amount', 'value'),
    Output('stocks-array', 'children'),

    Input('submit-val', 'n_clicks'),
    State('stock-name', 'value'),
    State('stock-buy-date', 'value'),
    State('stock-price', 'value'),
    State('stock-amount', 'value')
)
def update_output(n_clicks, name, date, price, amount):
    if (name is not None 
        and date is not None
        and price is not None
        and amount is not None ):
        
            
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


    return 'Purchased {} items of "{}" stock, on {} each priced as {}'.format(
        amount, name, date, price, n_clicks
    ), '', '', 0, 0, str(all_stocks)

@app.callback(
    Output('load-output-area', 'children'),
    Input('data-load', 'n_clicks')
)
def calcualte_data(n_clicks):
    if n_clicks > 0:

        sdl.run_data_load(all_stocks)
        

        with open('initial_positions.json', 'w') as fp:
            json.dump(all_stocks, fp, sort_keys=True, indent=4)
        return 'Data Load has been Completed!'


app.run_server(debug=False, host='0.0.0.0', port = 80)