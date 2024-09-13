from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)
app.title = "Medal Analysis Dashboard"
server = app.server

# Load the dataset
df = pd.read_csv("https://github.com/your-repo/cleaned_medals.csv")

image_path = 'assets/logo-mmu.png'

app.layout = html.Div([
    html.H1('MCM7183 Exercise 3'),
    html.Img(src=image_path),
    dcc.Dropdown(['Malaysia', 'Indonesia', 'China'], 'Malaysia', id='dropdown-country'),
    dcc.Graph(id="graph-scatter"),
    dcc.Slider(min=1960, max=2020, step=10, value=2020, marks={i: str(i) for i in range(1960, 2021, 10)}, id='slider-year'),
    dcc.Graph(id="graph-pie")
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
