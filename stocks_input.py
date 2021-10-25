from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


app = Dash(__name__)


def serve_layout(): 
    return html.Div([
    html.Div(dcc.Input(id='stock-name', type='text')),
    html.Div(dcc.Input(id='stock-buy-date', type='text')),
    html.Div(dcc.Input(id='stock-price', type='number')),
    html.Div(dcc.Input(id='stock-amount', type='number')),
    html.Div(id='stocks-array', children="array will appear here"),

    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])

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


if __name__ == '__main__':
    app.run_server(debug=True)