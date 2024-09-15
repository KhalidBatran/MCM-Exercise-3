import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

# Load your data
url = "https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv"
df = pd.read_csv(url)

# Convert data types if necessary
df['Country Code'] = df['Country Code'].astype(str)  # Ensure country codes are string if they are numeric
df['Medal Date'] = pd.to_datetime(df['Medal Date'])  # Convert dates if they are not in datetime format

# Example of preparing data for a slider or dropdown that needs integer keys
slider_marks = {int(i): {'label': str(date.strftime('%b %d'))} for i, date in enumerate(df['Medal Date'].dt.date.unique())}

# Initialize the Dash app (assuming it's not already running)
app = dash.Dash(__name__)
server = app.server  # Define the server to be used by Gunicorn

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
    filtered_df = df[df['Medal Date'].dt.strftime('%b %d') == date_selected]
    
    # Generate figure
    figure = {
        'data': [
            {'x': filtered_df['Country Code'], 'y': filtered_df['Medal Count'], 'type': 'bar', 'name': 'Medals'}
        ],
        'layout': {
            'title': 'Medal Count by Country for ' + date_selected
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
