from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)
app.title = "Medal Analysis Dashboard"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

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
        min=df['Medal Date'].min().year,
        max=df['Medal Date'].max().year,
        step=1,
        value=df['Medal Date'].max().year,
        marks={str(year): str(year) for year in range(df['Medal Date'].min().year, df['Medal Date'].max().year + 1, 5)}
    ),
    
    dcc.Graph(id="medal-timeline")
])

@callback(
    Output('graph-scatter', 'figure'),
    Output('graph-pie', 'figure'),
    Input('dropdown-country', 'value'),
    Input('slider-year', 'value'),
)
def update_graph(country_selected, year_selected):
    # Filter data for the selected country
    subset_Country = df[df['country'] == country_selected]
    
    # Create scatter plot for GDP over time
    fig = px.scatter(subset_Country, x="year", y="gdp", title=f'GDP over time for {country_selected}')
    
    # Filter data for the selected year
    subset_Year = df[df['year'] == year_selected]
    
    # Create pie chart data based on continent for the selected year
    pie_data = {
        "Asia": subset_Year[subset_Year['state'] == 'Asia']['gdp'].sum(),
        "Africa": subset_Year[subset_Year['state'] == 'Africa']['gdp'].sum(),
        "America": subset_Year[subset_Year['state'] == 'America']['gdp'].sum(),
        "Europe": subset_Year[subset_Year['state'] == 'Europe']['gdp'].sum(),
        "Oceania": subset_Year[subset_Year['state'] == 'Oceania']['gdp'].sum(),
    }
    
    pie_df = pd.DataFrame(list(pie_data.items()), columns=['Continent', 'GDP'])
    
    # Create pie chart
    fig2 = px.pie(pie_df, values="GDP", names="Continent", title=f'GDP distribution by continent in {year_selected}')
    
    return fig, fig2

if __name__ == '__main__':
    app.run(debug=True)
