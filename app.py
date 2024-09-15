import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

# Load your data
url = "https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv"
df = pd.read_csv(url)

# Convert data types if necessary
df['Country Code'] = df['Country Code'].astype(str)  # Ensure country codes are string if they are numeric
df['Medal Date'] = pd.to_datetime(df['Medal Date'])  # Convert dates if they are not in datetime format

# Prepare slider marks and convert to proper format
df['date_str'] = df['Medal Date'].dt.strftime('%b %d')
unique_dates = df['date_str'].unique()
slider_marks = {i: {'label': date} for i, date in enumerate(unique_dates)}

# Initialize the Dash app (assuming it's not already running)
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='medal-graph'),
    dcc.Slider(
        id='date-slider',
        min=0,
        max=len(slider_marks) - 1,
        value=0,
        marks=slider_marks,
        step=None
    )
])

@app.callback(
    Output('medal-graph', 'figure'),
    [Input('date-slider', 'value')]
)
def update_graph(slider_value):
    # Filter data based on slider
    date_selected = list(slider_marks.values())[slider_value]['label']
    filtered_df = df[df['date_str'] == date_selected]
    
    # Generate figure
    figure = {
        'data': [
            {'x': filtered_df['Country Code'], 'y': filtered_df['Total Medals'], 'type': 'bar', 'name': 'Medals'}
        ],
        'layout': {
            'title': 'Medal Count by Country for ' + date_selected
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
