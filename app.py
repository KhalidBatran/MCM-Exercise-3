import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympics 2024"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Ensure that 'Medal Date' is in datetime format
df['Medal Date'] = pd.to_datetime(df['Medal Date'])

# Extract day and month from 'Medal Date' and create a new column for display
df['Day Month'] = df['Medal Date'].dt.strftime('%d %b')  # Format as 'Day Month' e.g., '27 July'

# App layout with the new line chart
app.layout = html.Div([
    html.H1("Olympic Athletes' Medal Progression by Date", style={'textAlign': 'center'}),
    
    # Dropdown to select a specific country (optional)
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': country, 'value': country} for country in df['Country Code'].unique()],
        value='All',
        clearable=False,
        style={'width': '50%', 'margin': '10px auto'},
        placeholder="Choose a country"
    ),
    
    # Line chart figure
    dcc.Graph(id='medals-line-chart')
])

# Callback to update the figure based on the selected country
@app.callback(
    Output('medals-line-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_line_chart(selected_country):
    # Filter data by selected country if any
    if selected_country != 'All':
        filtered_df = df[df['Country Code'] == selected_country]
    else:
        filtered_df = df
    
    # Create the line chart
    fig = px.line(
        filtered_df,
        x='Day Month',  # Day and Month as the x-axis
        y=None,  # Since we're just showing progression by date, no y-value (can count occurrences if needed)
        color='Athlete Name',  # Each line represents an athlete
        markers=True,  # Add markers to show each point
        title=f"Medal Progression for {selected_country}" if selected_country != 'All' else "Medal Progression for All Countries",
        labels={'Day Month': 'Medal Date', 'count': 'Number of Medals'}
    )
    
    # Update x-axis to show the dates in order
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=sorted(df['Day Month'].unique()))
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
