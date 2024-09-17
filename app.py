import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load your data
url = "https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv"
df = pd.read_csv(url)

# Convert data types if necessary
df['Country Code'] = df['Country Code'].astype(str)  # Ensure country codes are string if they are numeric
df['Medal Date'] = pd.to_datetime(df['Medal Date'])  # Convert dates if they are not in datetime format

# App setup
app = dash.Dash(__name__)
server = app.server  # Add this line to define 'server'

# Layout
app.layout = html.Div([
    dcc.Graph(id='medal-graph'),
    dcc.Slider(
        id='date-slider',
        min=0,
        max=len(df['Medal Date'].dt.date.unique()) - 1,
        value=0,
        marks={i: {'label': date.strftime('%b %d')} for i, date in enumerate(sorted(df['Medal Date'].dt.date.unique()))},
        step=None
    ),
    dcc.Dropdown(
        id='medal-type-dropdown',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Gold', 'value': 'Gold'},
            {'label': 'Silver', 'value': 'Silver'},
            {'label': 'Bronze', 'value': 'Bronze'}
        ],
        value='All'  # Default value is now 'All'
    )
])

# Callback for updating the graph
@app.callback(
    Output('medal-graph', 'figure'),
    [Input('date-slider', 'value'), Input('medal-type-dropdown', 'value')]
)
def update_graph(slider_value, medal_type):
    date_selected = df['Medal Date'].dt.date.unique()[slider_value]
    filtered_df = df[df['Medal Date'].dt.date == date_selected]
    if medal_type != 'All':
        filtered_df = filtered_df[filtered_df['Medal Type'] == medal_type]
    figure = px.bar(
        filtered_df,
        x='Country Code',
        y='Count',
        color='Medal Type',
        title=f'Medal Distribution on {date_selected.strftime("%B %d, %Y")}'
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
