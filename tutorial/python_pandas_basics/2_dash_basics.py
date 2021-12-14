

# Dash basics
import plotly.graph_objects as go
from dash import Dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html


from pandas_datareader import data
def flatten_df(df):
    res_df = df
    res_df = res_df.reset_index()
    res_df = res_df[['Close', 'Date']]
    res_df.columns.droplevel()
    res_df.columns = res_df.columns.droplevel()
    res_df = res_df.rename(columns = {'':'Date'})
    return res_df
tickers = ['MSFT', 'AMZN', 'TSLA', 'GOOG', 'AAPL']
df = data.get_data_yahoo(tickers, '2021-08-01', '2021-08-30')
df_clean = flatten_df(df)


app = Dash(__name__)
app.title = "Portfolio Analytics"

def serve_layout(): 
    return dbc.Container([
        html.H1("Awesome H1 title here"),
        html.H3("Yet another awesome h3 title here"),
        
        #
        html.Div(id="output-div", children = "Changes will appear here"),

        ###
        html.Div(dcc.Graph(id="output-graph"
        )),
        ###
        dcc.Dropdown(
            id="drop_tickers_input",
            options=[{"label": i, "value": i} for i in tickers],
            value=tickers[0],
            clearable=False,
            className = 'text-dark',
        ),

        dcc.Dropdown(
            id="drop_input",
            options=[{"label": i, "value": i} for i in [1, 2, 3, 4, 5]],
            #value=1,
            clearable=False,
            className = 'text-dark',
        )
    ])
app.layout = serve_layout()
#app.run_server(debug=False, host='0.0.0.0', port = 88)


# Dash reactive

from dash import Input, Output, State

@app.callback(
    Output('output-div', 'children'),
    Input('drop_input', 'value'),
)
def get_output_dropdown(_input):
    if _input != None:
        output_text = 'You have selected: ' + str(_input)
        return output_text




##
@app.callback(
    Output('output-graph', 'figure'),
    Input('drop_tickers_input', 'value'),
)
def get_output_graph(_input):
    

    fig = go.Figure()

    if _input != None:
        fig.add_trace(go.Scatter(x=df_clean['Date'], y=df_clean[_input], name = 'My Dynamic Graph', mode='lines'))

    else:
        fig.add_trace(go.Scatter(x=df_clean['Date'], y=df_clean['MSFT'], name = 'My Dynamic Graph', mode='lines'))
        

    return fig

app.run_server(debug=False, host='0.0.0.0', port = 88)