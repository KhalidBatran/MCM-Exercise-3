import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

url = "https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv"
df = pd.read_csv(url)

# Convert and clean up the data as necessary
df['Country Code'] = df['Country Code'].astype(str)
df['Gender'] = df['Gender'].astype(str)
df['Medal Type'] = df['Medal Type'].astype(str)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Olympics Medal Dashboard", className="text-center"),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': x, 'value': x} for x in df['Country Code'].unique()],
            value='All',
            multi=False,
            placeholder='Select a Country',
        ), width=4),
        dbc.Col(dcc.Dropdown(
            id='gender-dropdown',
            options=[{'label': x, 'value': x} for x in df['Gender'].unique()],
            value='All',
            multi=False,
            placeholder='Select Gender',
        ), width=4),
        dbc.Col(dcc.Dropdown(
            id='medal-dropdown',
            options=[{'label': 'All', 'value': 'All'}] + [{'label': x, 'value': x} for x in df['Medal Type'].unique()],
            value='All',
            multi=False,
            placeholder='Select Medal Type',
        ), width=4),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='medal-graph'), width=12)
    ])
])

@app.callback(
    Output('medal-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('gender-dropdown', 'value'),
     Input('medal-dropdown', 'value')]
)
def update_graph(selected_country, selected_gender, selected_medal):
    filtered_df = df
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_medal != 'All':
        filtered_df = filtered_df[filtered_df['Medal Type'] == selected_medal]

    fig = px.bar(filtered_df, x='Country Code', y='Total Medals', color='Medal Type', 
                 title="Medals Distribution",
                 labels={'Total Medals': 'Total Medals', 'Country Code': 'Country Code'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
