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

    # Dropdowns for filtering
    html.Div([
        dcc.Dropdown(
            id='dropdown-country',
            options=[{'label': 'All Countries', 'value': 'ALL'}] + 
                    [{'label': country, 'value': country} for country in df['Country Code'].unique()],
            value='ALL',
            placeholder='Select a Country',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='dropdown-gender',
            options=[{'label': 'All Genders', 'value': 'ALL'}] + 
                    [{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
            value='ALL',
            placeholder='Select Gender',
            style={'width': '30%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='dropdown-medal-type',
            options=[{'label': 'All Medals', 'value': 'ALL'}, 
                     {'label': 'Gold', 'value': 'Gold Medal'},
                     {'label': 'Silver', 'value': 'Silver Medal'},
                     {'label': 'Bronze', 'value': 'Bronze Medal'}],
            value='ALL',
            placeholder='Select Medal Type',
            style={'width': '30%', 'display': 'inline-block'}
        ),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '10px'}),
    
    dcc.Graph(id="medal-count-by-country"),

    dcc.Graph(id="medals-by-gender"),

    dcc.Graph(id="medals-by-discipline"),

    dcc.Slider(
        id='slider-year',
        min=df['Medal Date'].dt.year.min(),
        max=df['Medal Date'].dt.year.max(),
        step=1,
        value=df['Medal Date'].dt.year.max(),
        marks={str(year): str(year) for year in range(df['Medal Date'].dt.year.min(), df['Medal Date'].dt.year.max() + 1, 5)},
    ),
    
    dcc.Graph(id="medal-timeline")
])

@callback(
    Output('medal-count-by-country', 'figure'),
    Output('medals-by-gender', 'figure'),
    Output('medals-by-discipline', 'figure'),
    Output('medal-timeline', 'figure'),
    Input('dropdown-country', 'value'),
    Input('dropdown-gender', 'value'),
    Input('dropdown-medal-type', 'value'),
    Input('slider-year', 'value'),
)
def update_graphs(selected_country, selected_gender, selected_medal, selected_year):
    # Apply filters
    filtered_df = df[df['Medal Date'].dt.year == selected_year]

    if selected_country != 'ALL':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_gender != 'ALL':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_medal != 'ALL':
        filtered_df = filtered_df[filtered_df['Medal Type'] == selected_medal]
    
    # First Figure: Total Medals by Country
    if selected_country == 'ALL':
        total_medals_by_country = filtered_df.groupby('Country Code')['Medal Type'].count().reset_index()
        fig_country = px.bar(total_medals_by_country, x='Country Code', y='Medal Type', title='Total Medals by Country')
    else:
        medals_by_type = filtered_df.groupby('Medal Type').count().reset_index()
        fig_country = px.bar(medals_by_type, x='Medal Type', y='Medal Date', title=f'Medal Count by Type for {selected_country}')
    
    # Second Figure: Medals by Gender (Fixed Colors)
    gender_medals = filtered_df.groupby('Medal Type').count().reset_index()
    fig_gender = px.pie(gender_medals, values='Medal Date', names='Medal Type', title=f'Medals by Gender: {selected_gender}')
    fig_gender.update_traces(marker=dict(colors=['green', 'red', 'blue']))

    # Third Figure: Medals by Discipline
    discipline_medals = filtered_df.groupby(['Sport Discipline', 'Country Code', 'Gender']).count().reset_index()
    fig_discipline = px.bar(discipline_medals, x='Sport Discipline', y='Medal Date', color='Country Code', title=f'Medals by Discipline')

    # Fourth Figure: Medal Timeline (Slider with Days and Months)
    timeline_filtered = df[df['Medal Date'].dt.year == selected_year]
    medal_timeline = timeline_filtered.groupby('Medal Date')['Medal Type'].count().reset_index()
    fig_timeline = px.line(medal_timeline, x='Medal Date', y='Medal Type', title=f'Medal Timeline for {selected_year}')

    return fig_country, fig_gender, fig_discipline, fig_timeline

if __name__ == '__main__':
    app.run(debug=True)
