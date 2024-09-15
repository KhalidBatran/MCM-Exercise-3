from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load the dataset
df = pd.read_csv('/mnt/data/cleaned_medals.csv')

# Convert 'Medal Date' to datetime and handle any errors by coercing invalid dates to NaT
df['Medal Date'] = pd.to_datetime(df['Medal Date'], errors='coerce')
df = df[df['Medal Date'].notna()]

app.layout = dbc.Container(
    [
        html.H1("Olympics 2024"),
        dcc.Tabs(
            [
                dcc.Tab(label="Medal Count by Country", value="tab-1"),
                dcc.Tab(label="Medals by Gender", value="tab-2"),
                dcc.Tab(label="Medals by Discipline", value="tab-3"),
                dcc.Tab(label="Medal Timeline", value="tab-4"),
            ],
            id="tabs",
            value="tab-1",
        ),
        dcc.Store(id="store"),
        html.Div(id="tab-content", className="p-4"),
    ]
)

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "value")]
)
def render_tab_content(active_tab):
    if active_tab == "tab-1":
        return html.Div([
            dcc.Dropdown(
                id='dropdown-country-1',
                options=[{'label': 'All Countries', 'value': 'ALL'}] + 
                        [{'label': country, 'value': country} for country in df['Country Code'].unique()],
                value='ALL',
                placeholder='Select a Country',
                style={'width': '30%', 'display': 'inline-block'}
            ),
            dcc.Dropdown(
                id='dropdown-gender-1',
                options=[{'label': 'All Genders', 'value': 'ALL'}] + 
                        [{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
                value='ALL',
                placeholder='Select Gender',
                style={'width': '30%', 'display': 'inline-block'}
            ),
            dcc.Dropdown(
                id='dropdown-medal-type-1',
                options=[{'label': 'All Medals', 'value': 'ALL'}, 
                         {'label': 'Gold', 'value': 'Gold Medal'},
                         {'label': 'Silver', 'value': 'Silver Medal'},
                         {'label': 'Bronze', 'value': 'Bronze Medal'}],
                value='ALL',
                placeholder='Select Medal Type',
                style={'width': '30%', 'display': 'inline-block'}
            ),
            dcc.Graph(id="medal-count-by-country")
        ])
    
    elif active_tab == "tab-2":
        return html.Div([
            dcc.Dropdown(
                id='dropdown-country-2',
                options=[{'label': 'All Countries', 'value': 'ALL'}] + 
                        [{'label': country, 'value': country} for country in df['Country Code'].unique()],
                value='ALL',
                placeholder='Select a Country',
                style={'width': '30%', 'display': 'inline-block'}
            ),
            dcc.Graph(id="medals-by-gender")
        ])

    elif active_tab == "tab-3":
        return html.Div([
            dcc.Dropdown(
                id='dropdown-discipline-3',
                options=[{'label': discipline, 'value': discipline} for discipline in df['Sport Discipline'].unique()],
                value=df['Sport Discipline'].unique()[0],
                placeholder='Select a Discipline',
                style={'width': '30%', 'display': 'inline-block'}
            ),
            dcc.Slider(
                id='slider-year-3',
                min=df['Medal Date'].dt.year.min(),
                max=df['Medal Date'].dt.year.max(),
                step=1,
                value=df['Medal Date'].dt.year.max(),
                marks={str(year): str(year) for year in range(df['Medal Date'].dt.year.min(), df['Medal Date'].dt.year.max() + 1, 4)},
            ),
            dcc.Graph(id="medals-by-discipline")
        ])

    elif active_tab == "tab-4":
        return html.Div([
            dcc.DatePickerRange(
                id='date-picker-4',
                min_date_allowed=df['Medal Date'].min().date(),
                max_date_allowed=df['Medal Date'].max().date(),
                start_date=df['Medal Date'].min().date(),
                end_date=df['Medal Date'].max().date()
            ),
            dcc.Graph(id="medal-timeline")
        ])

@app.callback(
    Output('medal-count-by-country', 'figure'),
    [Input('dropdown-country-1', 'value'),
     Input('dropdown-gender-1', 'value'),
     Input('dropdown-medal-type-1', 'value')]
)
def update_country_medals(selected_country, selected_gender, selected_medal):
    filtered_df = df.copy()

    if selected_country != 'ALL':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_gender != 'ALL':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_medal != 'ALL':
        filtered_df = filtered_df[filtered_df['Medal Type'] == selected_medal]

    fig_country = px.bar(filtered_df, x='Medal Type', y='Athlete Name', color='Gender',
                         title=f'Medals by Country and Gender: {selected_country}',
                         barmode='group')
    return fig_country

@app.callback(
    Output('medals-by-gender', 'figure'),
    [Input('dropdown-country-2', 'value')]
)
def update_gender_medals(selected_country):
    filtered_df = df.copy()

    if selected_country != 'ALL':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]

    fig_gender = px.bar(filtered_df, x='Gender', y='Medal Type', color='Sport Discipline',
                        title=f'Medals by Gender and Sport for {selected_country}')
    return fig_gender

@app.callback(
    Output('medals-by-discipline', 'figure'),
    [Input('dropdown-discipline-3', 'value'),
     Input('slider-year-3', 'value')]
)
def update_discipline_medals(selected_discipline, selected_year):
    filtered_df = df[(df['Sport Discipline'] == selected_discipline) & (df['Medal Date'].dt.year == selected_year)]

    fig_discipline = px.bar(filtered_df, x='Country Code', y='Medal Type', color='Gender',
                            title=f'Medals by Discipline and Year: {selected_discipline} in {selected_year}')
    return fig_discipline

@app.callback(
    Output('medal-timeline', 'figure'),
    [Input('date-picker-4', 'start_date'),
     Input('date-picker-4', 'end_date')]
)
def update_timeline(start_date, end_date):
    filtered_df = df[(df['Medal Date'] >= start_date) & (df['Medal Date'] <= end_date)]

    fig_timeline = px.line(filtered_df, x='Medal Date', y='Medal Type', color='Country Code',
                           title=f'Medal Timeline from {start_date} to {end_date}')
    return fig_timeline

if __name__ == "__main__":
    app.run_server(debug=True)
