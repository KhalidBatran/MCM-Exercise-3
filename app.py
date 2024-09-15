from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)
app.title = "Olympics 2024"
server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv')
df['Medal Date'] = pd.to_datetime(df['Medal Date'], errors='coerce')
df = df[df['Medal Date'].notna()]

app.layout = html.Div([
    html.H1('Olympics 2024'),

    dcc.Tabs([
        dcc.Tab(label='Medal Count by Country', children=[
            dcc.Dropdown(
                id='dropdown-country',
                options=[{'label': 'All Countries', 'value': 'All'}] + [{'label': c, 'value': c} for c in df['Country Code'].unique()],
                value='All',
                style={'width': '50%'}
            ),
            dcc.Dropdown(
                id='dropdown-medal-type',
                options=[{'label': 'All Medals', 'value': 'All'}] + [{'label': m, 'value': m} for m in df['Medal Type'].unique()],
                value='All',
                style={'width': '50%'}
            ),
            dcc.Graph(id='medal-count-by-country-graph')
        ]),
        dcc.Tab(label='Medals by Discipline', children=[
            dcc.Slider(
                id='date-slider',
                min=df['Medal Date'].dt.dayofyear.min(),
                max=df['Medal Date'].dt.dayofyear.max(),
                value=df['Medal Date'].dt.dayofyear.min(),
                marks={d: {'label': date.strftime('%b %d')} for d, date in zip(df['Medal Date'].dt.dayofyear.unique(), df['Medal Date'].unique())},
                step=None
            ),
            dcc.Graph(id='medals-by-discipline-graph')
        ]),
        dcc.Tab(label='Medal Timeline', children=[
            dcc.Graph(id='medal-timeline-graph')
        ])
    ])
])

@callback(
    Output('medal-count-by-country-graph', 'figure'),
    Input('dropdown-country', 'value'),
    Input('dropdown-medal-type', 'value')
)
def update_medal_count_by_country(selected_country, selected_medal_type):
    filtered_df = df if selected_country == 'All' else df[df['Country Code'] == selected_country]
    filtered_df = filtered_df if selected_medal_type == 'All' else filtered_df[filtered_df['Medal Type'] == selected_medal_type]
    fig = px.bar(filtered_df, x='Country Code', y='Medal Type', title="Medals by Country")
    return fig

@callback(
    Output('medals-by-discipline-graph', 'figure'),
    Input('date-slider', 'value')
)
def update_medals_by_discipline(selected_date):
    filtered_df = df[df['Medal Date'].dt.dayofyear == selected_date]
    fig = px.bar(filtered_df, x='Discipline', y='Medal Type', color='Country Code', title="Medals by Discipline")
    return fig

@callback(
    Output('medal-timeline-graph', 'figure'),
    Input('date-slider', 'value')
)
def update_medal_timeline(selected_date):
    filtered_df = df[df['Medal Date'].dt.dayofyear == selected_date]
    fig = px.line(filtered_df, x='Medal Date', y='Medal Type', color='Country Code', title="Medal Timeline")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
