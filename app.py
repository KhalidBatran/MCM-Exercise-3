import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympics 2024"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Ensure 'Medal Date' is in datetime format and format it as 'Day Month'
df['Medal Date'] = pd.to_datetime(df['Medal Date']).dt.strftime('%d %B')

# Layout of the app
app.layout = html.Div([
    html.H1("Comparison of Genders and Medals", style={'textAlign': 'center'}),
    
    # Multi-select dropdown to filter by country
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': country, 'value': country} for country in df['Country Code'].unique()],
        value=['All'],  # Default to all countries
        clearable=False,
        multi=True,  # Enable multi-selection
        style={'width': '50%', 'margin': '10px auto'},
        placeholder="Choose country or countries"
    ),
    
    # Figure: Compare between Genders and Medals
    dcc.Graph(id='gender-medal-bar-chart')
])

# Callback to generate the figure (Gender vs Medals comparison)
@app.callback(
    Output('gender-medal-bar-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_gender_medal_chart(selected_countries):
    # Filter data by selected countries
    if 'All' in selected_countries or not selected_countries:
        filtered_df = df
    else:
        filtered_df = df[df['Country Code'].isin(selected_countries)]

    # Create a grouped bar chart to compare genders and medals
    fig = px.bar(
        filtered_df,
        x='Medal Type',  # X-axis: Medal Type (Gold, Silver, Bronze)
        y='Medal Type',  # The count of medals will be automatically calculated
        color='Gender',  # Bars grouped by Gender (Male, Female)
        barmode='group',  # Grouped bar mode to compare Male vs Female
        title="Comparison of Genders and Medals",
        labels={'Medal Type': 'Medal Type', 'count': 'Number of Medals'},
        category_orders={"Medal Type": ["Gold Medal", "Silver Medal", "Bronze Medal"]},  # Consistent order of medals
        color_discrete_map={'M': 'blue', 'F': 'pink'}  # Custom colors for Male and Female
    )

    # Enhanced hover details
    fig.update_traces(
        hovertemplate=(
            '<b>Athlete Name:</b> %{customdata[0]}<br>' +
            '<b>Medal Date:</b> %{customdata[1]}<br>' +
            '<b>Sport Discipline:</b> %{customdata[2]}<br>'
        ),
        customdata=filtered_df[['Athlete Name', 'Medal Date', 'Sport Discipline']].values  # Add additional data to hover
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
