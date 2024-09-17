from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Stacked Bar Chart"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Unique sports and countries for dropdown
sports = df['Sport Discipline'].unique()
countries = df['Country Code'].unique()

sports_options = [{'label': 'All', 'value': 'All'}] + [{'label': sport, 'value': sport} for sport in sports]
country_options = [{'label': 'All', 'value': 'All'}] + [{'label': country, 'value': country} for country in countries]

app.layout = html.Div([
    html.H1("Olympic Medals by Country and Sport", style={'textAlign': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='sport-dropdown',
            options=sports_options,
            value='All',  # Default to 'All'
            clearable=False,
            multi=True,  # Allow multiple selections
            style={'width': '45%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='country-dropdown',
            options=country_options,
            value='All',  # Default to 'All'
            clearable=False,
            multi=True,  # Allow multiple selections
            style={'width': '45%', 'display': 'inline-block'}
        )
    ]),
    dcc.Graph(id='medals-stacked-bar')
])

@app.callback(
    Output('medals-stacked-bar', 'figure'),
    [Input('sport-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_stacked_bar(selected_sports, selected_countries):
    # Filter by sport
    if 'All' in selected_sports or not selected_sports:
        filtered_df = df
    else:
        filtered_df = df[df['Sport Discipline'].isin(selected_sports)]
    
    # Filter by country
    if 'All' not in selected_countries and selected_countries:
        filtered_df = filtered_df[filtered_df['Country Code'].isin(selected_countries)]
    
    # Prepare data for the stacked bar chart
    bar_data = filtered_df.groupby(['Country Code', 'Medal Type']).size().reset_index(name='Counts')
    bar_data = bar_data.pivot(index='Country Code', columns='Medal Type', values='Counts').fillna(0)
    
    # Create the stacked bar chart
    fig = px.bar(bar_data, x=bar_data.index, y=['Gold Medal', 'Silver Medal', 'Bronze Medal'],
                 title="Medal Counts by Country for Selected Sports",
                 labels={'value': 'Number of Medals', 'Country Code': 'Country'},
                 color_discrete_map={'Gold Medal': 'gold', 'Silver Medal': 'silver', 'Bronze Medal': '#cd7f32'})
    fig.update_layout(barmode='stack')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
