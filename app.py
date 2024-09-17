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

# Ensure 'Medal Date' is in datetime format and convert it to 'Day Month' format
df['Medal Date'] = pd.to_datetime(df['Medal Date'])
df['Medal Date'] = df['Medal Date'].dt.strftime('%d %B')  # Format as 'Day Month'

# Ensure that all medal types are properly labeled and included
df['Medal Type'] = df['Medal Type'].replace({
    'G': 'Gold Medal',
    'S': 'Silver Medal',
    'B': 'Bronze Medal'
})

# Layout of the app
app.layout = html.Div([
    html.H1("Comparison of Genders and Medals", style={'textAlign': 'center'}),
    
    # Dropdown to filter by country with multi-select enabled
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': country, 'value': country} for country in df['Country Code'].unique()],
        value=['All'],  # Default to all countries
        clearable=False,
        multi=True,  # Enable multi-select
        style={'width': '50%', 'margin': '10px auto'},
        placeholder="Choose a country or countries"
    ),
    
    # Gender and Medals comparison bar chart
    dcc.Graph(id='gender-medal-bar-chart')
])

# Callback to generate the third figure (Gender vs Medals comparison)
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
        labels={'Medal Type': 'Medal', 'count': 'Total Medals'},
        category_orders={"Medal Type": ["Gold Medal", "Silver Medal", "Bronze Medal"]},  # Consistent order of medals
        color_discrete_map={'M': 'blue', 'F': 'pink'}  # Custom colors for Male and Female
    )
    
    # Update layout to correctly display medal types and address misplaced labels
    fig.update_layout(
        yaxis_title='Total Medals',  # Correct y-axis title
        xaxis_title='Medal Type',  # Correct x-axis title
        xaxis={'categoryorder': 'total descending'}  # Sort categories by total medals descending
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
