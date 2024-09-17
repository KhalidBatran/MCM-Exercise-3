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

# Layout of the app
app.layout = html.Div([
    html.H1("Olympic Athletes' Medal Progression by Date", style={'textAlign': 'center'}),

    # Slider to filter by date
    dcc.Slider(
        id='date-slider',
        min=0,
        max=len(df['Medal Date'].dt.date.unique()) - 1,
        value=0,
        marks={i: {'label': date.strftime('%b %d')} for i, date in enumerate(sorted(df['Medal Date'].dt.date.unique()))},
        step=None
    ),

    # Line chart figure
    dcc.Graph(id='medals-line-chart')
])

# Callback to update the line chart based on the slider value
@app.callback(
    Output('medals-line-chart', 'figure'),
    Input('date-slider', 'value')
)
def update_line_chart(slider_value):
    # Get the selected date based on slider position
    date_selected = df['Medal Date'].dt.date.unique()[slider_value]
    
    # Filter data by the selected date
    filtered_df = df[df['Medal Date'].dt.date == date_selected]
    
    # Create the line chart with enhanced hover interaction
    fig = px.line(
        filtered_df,
        x='Day Month',  # Day and month as the x-axis
        y=None,  # No y-value (we're just showing the medal progression)
        color='Athlete Name',  # Color the lines based on the athlete
        markers=True,  # Add markers to show each point
        title=f"Medal Progression for {date_selected.strftime('%B %d, %Y')}",
        labels={'Day Month': 'Medal Date'},
        hover_data={  # Add details to the hover interaction
            'Medal Type': True,  # Show medal type (Gold, Silver, Bronze)
            'Gender': True,  # Show the athlete's gender
            'Sport Discipline': True  # Show the sport in which the medal was won
        }
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
