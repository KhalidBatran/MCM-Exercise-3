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

# Ensure 'Medal Date' is in datetime format
df['Medal Date'] = pd.to_datetime(df['Medal Date'])

# Extract day and month from 'Medal Date' and create a new column for display
df['Day Month'] = df['Medal Date'].dt.strftime('%d %b')  # Format as 'Day Month'

# Generate marks for the slider with 'All' as the first option
slider_marks = {i: {'label': date.strftime('%b %d')} for i, date in enumerate(sorted(df['Medal Date'].dt.date.unique()))}
slider_marks[-1] = {'label': 'All'}  # Add 'All' at the end

# Layout of the app
app.layout = html.Div([
    html.H1("Olympic Athletes' Medal Progression by Date", style={'textAlign': 'center'}),
    
    # Dropdown to filter by country
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': country, 'value': country} for country in df['Country Code'].unique()],
        value='All',  # Default to all countries
        clearable=False,
        style={'width': '50%', 'margin': '10px auto'},
        placeholder="Choose a country"
    ),
    
    # Line chart figure
    dcc.Graph(id='medals-line-chart'),
    
    # Slider to filter by date (placed under the figure)
    dcc.Slider(
        id='date-slider',
        min=-1,  # Start with 'All'
        max=len(df['Medal Date'].dt.date.unique()) - 1,
        value=-1,  # Default to 'All'
        marks=slider_marks,  # Marks include 'All' and all dates
        step=None
    )
])

# Callback to update the line chart based on the slider value and country filter
@app.callback(
    Output('medals-line-chart', 'figure'),
    [Input('date-slider', 'value'), Input('country-dropdown', 'value')]
)
def update_line_chart(slider_value, selected_country):
    # Default behavior: show all dates when "All" is selected
    if slider_value == -1:
        filtered_df = df if selected_country == 'All' else df[df['Country Code'] == selected_country]
        
        # Normal line chart, X is Medal Date and Y is Index
        fig = px.line(
            filtered_df,
            x='Day Month',  # Day and month as the x-axis
            y=filtered_df.index,  # Use index as y-axis
            color='Athlete Name',  # Color the lines based on the athlete
            markers=True,  # Add markers to show each point
            title=f"Medal Progression for {selected_country}" if selected_country != 'All' else "Medal Progression for All Countries",
            labels={'Day Month': 'Medal Date'},
            hover_data={  # Add details to the hover interaction
                'Medal Type': True,
                'Gender': True,
                'Sport Discipline': True
            }
        )
    
    # When a specific date is selected
    else:
        date_selected = df['Medal Date'].dt.date.unique()[slider_value]
        filtered_df = df[(df['Medal Date'].dt.date == date_selected)]
        if selected_country != 'All':
            filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
        
        # Separate the dots by using Sport Discipline on X and medals on Y
        fig = px.scatter(
            filtered_df,
            x='Sport Discipline',  # Use Sport as the x-axis when a specific date is selected
            y='Medal Type',  # Separate by medals on the y-axis
            color='Athlete Name',  # Each point represents an athlete
            title=f"Medal Details on {date_selected.strftime('%B %d, %Y')} for {selected_country}",
            labels={'Sport Discipline': 'Sport', 'Medal Type': 'Medal'},
            hover_data={  # Enhanced hover with additional details
                'Medal Type': True,
                'Gender': True,
                'Sport Discipline': True
            }
        )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
