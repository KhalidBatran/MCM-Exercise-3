import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.graph_objs as go

url = "https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv"
df = pd.read_csv(url)

df['Country Code'] = df['Country Code'].astype(str)
df['Medal Date'] = pd.to_datetime(df['Medal Date'])
df['date_str'] = df['Medal Date'].dt.strftime('%b %d')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Olympics Medal Dashboard", className="text-center"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in df['Country Code'].unique()],
                value=None,
                placeholder="Select a country",
                multi=True
            ),
            dcc.Dropdown(
                id='gender-dropdown',
                options=[{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
                value=None,
                placeholder="Select a gender",
                multi=True
            ),
            dcc.Dropdown(
                id='medal-dropdown',
                options=[{'label': medal, 'value': medal} for medal in df['Medal Type'].unique()],
                value=None,
                placeholder="Select medal type",
                multi=True
            ),
            dcc.Graph(id='medal-graph')
        ], width=12)
    ])
])

@app.callback(
    Output('medal-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('gender-dropdown', 'value'),
     Input('medal-dropdown', 'value')]
)
def update_graph(selected_countries, selected_genders, selected_medals):
    filtered_df = df
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country Code'].isin(selected_countries)]
    if selected_genders:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]
    if selected_medals:
        filtered_df = filtered_df[filtered_df['Medal Type'].isin(selected_medals)]
    
    figure = go.Figure(
        data=[
            go.Bar(
                x=filtered_df['Country Code'],
                y=filtered_df['Total Medals'],
                name='Medals',
                marker=dict(color=filtered_df['Medal Type'].map({'Gold': 'gold', 'Silver': 'silver', 'Bronze': '#cd7f32'}))
            )
        ],
        layout=go.Layout(
            title='Medal Count by Country',
            xaxis=dict(title='Country Code'),
            yaxis=dict(title='Total Medals'),
            barmode='stack'
        )
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
