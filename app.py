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

# Filter out rows where 'Medal Date' is NaT (invalid dates)
df = df[df['Medal Date'].notna()]

app.layout = html.Div([
    html.H1('Medal Analysis Dashboard'),
    
    dcc.Dropdown(
        id='dropdown-country',
        options=[{'label': country, 'value': country} for country in df['Country Code'].unique()],
        value='USA',
        placeholder='Select a Country'
    ),
    
    dcc.Graph(id="medal-count-by-country"),
    
    dcc.Dropdown(
        id='dropdown-gender',
        options=[{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
        value='M',
        placeholder='Select Gender'
    ),
    
    dcc.Graph(id="medals-by-gender"),
    
    dcc.Dropdown(
        id='dropdown-discipline',
        options=[{'label': discipline, 'value': discipline} for discipline in df['Sport Discipline'].unique()],
        value='Cycling',
        placeholder='Select Discipline'
    ),
    
    dcc.Graph(id="medals-by-discipline"),
    
    dcc.Slider(
        id='slider-year',
        min=df['Medal Date'].dt.year.min(),
        max=df['Medal Date'].dt.year.max(),
        step=1,
        value=df['Medal Date'].dt.year.max(),
        marks={str(year): str(year) for year in range(df['Medal Date'].dt.year.min(), df['Medal Date'].dt.year.max() + 1, 5)}
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
    Input('dropdown-discipline', 'value'),
    Input('slider-year', 'value'),
)
def update_graphs(selected_country, selected_gender, selected_discipline, selected_year):
    # Medal count by country
    country_filtered = df[df['Country Code'] == selected_country]
    medal_count_by_country = country_filtered.groupby('Medal Type').count().reset_index()
    fig_country = px.bar(medal_count_by_country, x='Medal Type', y='Medal Date', title=f'Medal Count by Type for {selected_country}')
    
    # Medals by gender
    gender_filtered = df[df['Gender'] == selected_gender]
    medals_by_gender = gender_filtered.groupby('Medal Type').count().reset_index()
    fig_gender = px.pie(medals_by_gender, values='Medal Date', names='Medal Type', title=f'Medals by Gender: {selected_gender}')
    
    # Medals by discipline
    discipline_filtered = df[df['Sport Discipline'] == selected_discipline]
    medals_by_discipline = discipline_filtered.groupby('Medal Type').count().reset_index()
    fig_discipline = px.bar(medals_by_discipline, x='Medal Type', y='Medal Date', title=f'Medals by Discipline: {selected_discipline}')
    
    # Medal timeline
    year_filtered = df[df['Medal Date'].dt.year == selected_year]
    medal_timeline = year_filtered.groupby('Medal Date')['Medal Type'].count().reset_index()
    fig_timeline = px.line(medal_timeline, x='Medal Date', y='Medal Type', title=f'Medal Timeline for {selected_year}')
    
    return fig_country, fig_gender, fig_discipline, fig_timeline

if __name__ == '__main__':
    app.run(debug=True)
