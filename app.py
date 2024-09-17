from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Define the app layout with navigation and content components
app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Heatmap", href="/")),
            dbc.NavItem(dbc.NavLink("Time Series", href="/time-series")),
            dbc.NavItem(dbc.NavLink("Bubble Chart", href="/bubble-chart")),
        ],
        brand="Olympic Medals Visualization",
        brand_href="/",
        color="primary",
        dark=True,
    ),
    dcc.Location(id="url"),
    html.Div(id="page-content")
])

# Define callback for dynamic page loading
@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/time-series":
        return html.Div([
            html.H1('Olympic Medals Time Series Analysis', style={'textAlign': 'center'}),
            dcc.Slider(
                id='year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].max(),
                marks={str(year): str(year) for year in df['Year'].unique()},
                step=None
            ),
            dcc.Graph(id="time-series-graph")
        ])
    elif pathname == "/bubble-chart":
        return html.Div([
            html.H1('Olympic Medals Bubble Chart', style={'textAlign': 'center'}),
            dcc.Checklist(
                id='country-checklist',
                options=[{'label': country, 'value': country} for country in df['Country Code'].unique()],
                value=[df['Country Code'].unique()[0]],
                inline=True
            ),
            dcc.Graph(id="bubble-chart-graph")
        ])
    # This assumes the "/" path will handle the heatmap
    else:
        return html.Div([
            html.H1('Olympic Medals Heatmap', style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
                value=df['Year'].max(),
                clearable=False
            ),
            dcc.Graph(id="heatmap-graph")
        ])

# Callback for the Heatmap page
@app.callback(
    Output('heatmap-graph', 'figure'),
    Input('year-dropdown', 'value'))
def update_heatmap(selected_year):
    filtered_df = df[df['Year'] == selected_year]
    fig = px.density_heatmap(filtered_df, x='Country Code', y='Sport Discipline', z='Count', histfunc='sum')
    return fig

# Callback for the Time Series page
@app.callback(
    Output('time-series-graph', 'figure'),
    Input('year-slider', 'value'))
def update_time_series(selected_year):
    filtered_df = df[df['Year'] == selected_year]
    fig = px.line(filtered_df, x='Date', y='Count', color='Medal Type')
    return fig

# Callback for the Bubble Chart page
@app.callback(
    Output('bubble-chart-graph', 'figure'),
    Input('country-checklist', 'value'))
def update_bubble_chart(selected_countries):
    filtered_df = df[df['Country Code'].isin(selected_countries)]
    fig = px.scatter(filtered_df, x='Sport Discipline', y='Athlete Name',
                     size='Count', color='Medal Type', hover_name='Athlete Name')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
