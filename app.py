import dash
import dash_auth
from dash import dcc
from dash import html
import pandas as pd
import plotly


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'Mickey': 'Mouse', 'Donald': 'Duck', 'Carlos': 'Santana'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Authorization Application'
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    html.H1('Welcome, if you are authorized!'),
    html.H3('You are successfully authorized'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in [1, 2, 3, 4]],
        value=1
    ),
    dcc.Graph(id='graph'),
    html.A('Code on Github', href='https://github.com/ksebastian/208-authentication-example'),
    html.Br(),
    html.A("Data Source", href='https://dash.plotly.com/authentication'),
], className='container')


def get_drinks_data():
    drinks = pd.read_csv('data/drinks.csv')
    sample = drinks.sample(10).to_records(index=False)
    return sample


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_graph(dropdown_value):
    drinks_data = get_drinks_data()
    x_values = list(zip(*drinks_data))[0]
    y_values = list(zip(*drinks_data))[dropdown_value]
    if dropdown_value == 1:
        title_value = 'Beer Servings'
        color_value = 'brown'
    elif dropdown_value == 2:
        title_value = 'Spirit Servings'
        color_value = 'blue'
    elif dropdown_value == 3:
        title_value = 'Wine Servings'
        color_value = 'red'
    elif dropdown_value == 4:
        title_value = 'Total Alcohol(litres)'
        color_value = 'yellow'

    #x_values = [-3,-2,-1,0,1,2,3]
    #y_values = [x**dropdown_value for x in x_values]
    return {
        'layout': {
            'title': 'Graph of {}'.format(title_value),
            'margin': {
                'l': 30,
                'b': 50,
                'r': 10,
                't': 60
            }
        },
        'data': [{'x': x_values, 'y': y_values, 'line': dict(color=color_value)}]
    }

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
