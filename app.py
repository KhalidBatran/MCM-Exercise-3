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
                options=[{'label': country, 'value': country} for country in df['Country Code'].unique()],
                value='All Countries',
                placeholder='Select a Country',
                style={'width': '50%'}
            ),
            dcc.Dropdown(
                id='dropdown-medal-type',
                options=[{'label': medal, 'value': medal} for medal in df['Medal Type'].unique()],
                value='All Medals',
                placeholder='Select Medal Type',
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
                marks={int(date): {'label': str(date)} for date in df['Medal Date'].dt.strftime('%b %d').unique()},
                step=None
            ),
            dcc.Graph(id='medals-by-discipline-graph')
        ]),
        dcc.Tab(label='Medal Timeline', children=[
            dcc.Dropdown(
                id='dropdown-timeline-type',
                options=[{'label': medal, 'value': medal} for medal in df['Medal Type'].unique()],
                value='All Medals',
                placeholder='Select Medal Type',
                style={'width': '50%'}
            ),
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
    filtered_df = df
    if selected_country != 'All Countries':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_medal_type != 'All Medals':
        filtered_df = filtered_df[filtered_df['Medal Type'] == selected_medal_type]
    fig = px.bar(filtered_df, x='Country Code', y='Count', color='Medal Type')
    return fig

@callback(
    Output('medals-by-discipline-graph', 'figure'),
    Input('date-slider', 'value')
)
def update_medals_by_discipline(selected_date):
    filtered_df = df[df['Medal Date'].dt.dayofyear == selected_date]
    fig = px.bar(filtered_df, x='Discipline', y='Count', color='Country Code')
    return fig

@callback(
    Output('medal-timeline-graph', 'figure'),
    Input('dropdown-timeline-type', 'value')
)
def update_medal_timeline(selected_medal_type):
    filtered_df = df
    if selected_medal_type != 'All Medals':
        filtered_df = filtered_df[filtered_df['Medal Type'] == selected_medal_type]
    fig = px.line(filtered_df, x='Medal Date', y='Count', color='Medal Type')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
