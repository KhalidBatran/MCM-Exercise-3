import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

app.layout = dbc.Container([
    html.H1("Olympic Medals Visualization", className="text-center"),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Scatter Plot', value='scatter'),
        dcc.Tab(label='Histogram', value='histogram'),
        dcc.Tab(label='Bar Plot', value='bar')
    ], active_tab='scatter'),
    html.Div(id='tab-content')
])

@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'active_tab')
)
def render_content(tab):
    if tab == 'scatter':
        fig = px.scatter(df, x='Athlete Name', y='Medal Type',
                         color='Gender', title='Scatter Plot: Medals by Athlete and Gender')
        return dcc.Graph(figure=fig)
    
    elif tab == 'histogram':
        fig = px.histogram(df, x='Medal Type', color='Country Code',
                           title='Histogram: Medal Count by Country')
        return dcc.Graph(figure=fig)
    
    elif tab == 'bar':
        fig = px.bar(df, x='Sport Discipline', y='Medal Type', color='Country Code',
                     title='Bar Plot: Medals by Sport and Country')
        return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run_server(debug=True)
