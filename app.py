from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)
app.title = "Medal Analysis Dashboard"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Convert 'Medal Date' to datetime and handle any errors by coercing invalid dates to NaT
df['Medal Date'] = pd.to_datetime(df['Medal Date'], errors='coerce')
df = df[df['Medal Date'].notna()]

app.layout = html.Div([
    html.H1('Medal Analysis Dashboard'),

    # First Figure: Medal Count by Country
    html.Div([
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
    ], style={'margin-bottom': '40px'}),

    # Second Figure: Medals by Gender
    html.Div([
        dcc.Dropdown(
            id='dropdown-country-2',
            options=[{'label': 'All Countries', 'value': 'ALL'}] + 
                    [{'label': country, 'value': country} for country in df['Country Code'].unique()],
            value='ALL',
            placeholder='Select a Country',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='dropdown-gender-2',
            options=[{'label': 'All Genders', 'value': 'ALL'}] + 
                    [{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
            value='ALL',
            placeholder='Select Gender',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='dropdown-medal-type-2',
            options=[{'label': 'All Medals', 'value': 'ALL'}, 
                     {'label': 'Gold', 'value': 'Gold Medal'},
                     {'label': 'Silver', 'value': 'Silver Medal'},
                     {'label': 'Bronze', 'value': 'Bronze Medal'}],
            value='ALL',
            placeholder='Select Medal Type',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Graph(id="medals-by-gender")
    ], style={'margin-bottom': '40px'}),

    # Third Figure: Medals by Discipline
    html.Div([
        dcc.Dropdown(
            id='dropdown-country-3',
            options=[{'label': 'All Countries', 'value': 'ALL'}] + 
                    [{'label': country, 'value': country} for country in df['Country Code'].unique()],
            value='ALL',
            placeholder='Select a Country',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='dropdown-gender-3',
            options=[{'label': 'All Genders', 'value': 'ALL'}] + 
                    [{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
            value='ALL',
            placeholder='Select Gender',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='dropdown-medal-type-3',
            options=[{'label': 'All Medals', 'value': 'ALL'}, 
                     {'label': 'Gold', 'value': 'Gold Medal'},
                     {'label': 'Silver', 'value': 'Silver Medal'},
                     {'label': 'Bronze', 'value': 'Bronze Medal'}],
            value='ALL',
            placeholder='Select Medal Type',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Graph(id="medals-by-discipline")
    ], style={'margin-bottom': '40px'}),

    # Fourth Figure: Medal Timeline (Slider with Days/Months)
    html.Div([
        dcc.Dropdown(
            id='dropdown-country-4',
            options=[{'label': 'All Countries', 'value': 'ALL'}] + 
                    [{'label': country, 'value': country} for country in df['Country Code'].unique()],
            value='ALL',
            placeholder='Select a Country',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='dropdown-gender-4',
            options=[{'label': 'All Genders', 'value': 'ALL'}] + 
                    [{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
            value='ALL',
            placeholder='Select Gender',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='dropdown-medal-type-4',
            options=[{'label': 'All Medals', 'value': 'ALL'}, 
                     {'label': 'Gold', 'value': 'Gold Medal'},
                     {'label': 'Silver', 'value': 'Silver Medal'},
                     {'label': 'Bronze', 'value': 'Bronze Medal'}],
            value='ALL',
            placeholder='Select Medal Type',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=df['Medal Date'].min().date(),
            max_date_allowed=df['Medal Date'].max().date(),
            start_date=df['Medal Date'].min().date(),
            end_date=df['Medal Date'].max().date()
        ),
        dcc.Graph(id="medal-timeline")
    ])
])

# Callbacks for individual figures
@callback(
    Output('medal-count-by-country', 'figure'),
    Input('dropdown-country-1', 'value'),
    Input('dropdown-gender-1', 'value'),
    Input('dropdown-medal-type-1', 'value'),
)
def update_country_medals(selected_country, selected_gender, selected_medal):
    filtered_df = df.copy()

    if selected_country != 'ALL':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_gender != 'ALL':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_medal != 'ALL':
        filtered_df = filtered_df[filtered_df['Medal Type'] == selected_medal]

    fig_country = px.bar(filtered_df.groupby('Country Code')['Medal Type'].count().reset_index(), x='Country Code', y='Medal Type', title='Total Medals by Country')
    return fig_country

@callback(
    Output('medals-by-gender', 'figure'),
    Input('dropdown-country-2', 'value'),
    Input('dropdown-gender-2', 'value'),
    Input('dropdown-medal-type-2', 'value'),
)
def update_gender_medals(selected_country, selected_gender, selected_medal):
    filtered_df = df.copy()

    if selected_country != 'ALL':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_gender != 'ALL':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_medal != 'ALL':
        filtered_df = filtered_df[filtered_df['Medal Type'] == selected_medal]

    fig_gender = px.pie(filtered_df.groupby('Medal Type').count().reset_index(), values='Medal Date', names='Medal Type', title='Medals by Gender')
    fig_gender.update_traces(marker=dict(colors=['green', 'red', 'blue']))
    return fig_gender

@callback(
    Output('medals-by-discipline', 'figure'),
    Input('dropdown-country-3', 'value'),
    Input('dropdown-gender-3', 'value'),
    Input('dropdown-medal-type-3', 'value'),
)
def update_discipline_medals(selected_country,
                                 selected_gender, selected_medal):
    filtered_df = df.copy()

    if selected_country != 'ALL':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_gender != 'ALL':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_medal != 'ALL':
        filtered_df = filtered_df[filtered_df['Medal Type'] == selected_medal]

    fig_discipline = px.bar(filtered_df.groupby(['Sport Discipline', 'Country Code', 'Gender']).count().reset_index(),
                            x='Sport Discipline', y='Medal Date', color='Country Code', title='Medals by Discipline')
    return fig_discipline

@callback(
    Output('medal-timeline', 'figure'),
    Input('dropdown-country-4', 'value'),
    Input('dropdown-gender-4', 'value'),
    Input('dropdown-medal-type-4', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
)
def update_timeline_medals(selected_country, selected_gender, selected_medal, start_date, end_date):
    filtered_df = df.copy()

    if selected_country != 'ALL':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_gender != 'ALL':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_medal != 'ALL':
        filtered_df = filtered_df[filtered_df['Medal Type'] == selected_medal]

    filtered_df = filtered_df[(filtered_df['Medal Date'] >= start_date) & (filtered_df['Medal Date'] <= end_date)]

    medal_timeline = filtered_df.groupby('Medal Date')['Medal Type'].count().reset_index()
    fig_timeline = px.line(medal_timeline, x='Medal Date', y='Medal Type', title='Medal Timeline')
    return fig_timeline

if __name__ == '__main__':
    app.run(debug=True)
