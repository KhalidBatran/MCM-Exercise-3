from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Visualization"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

app.layout = html.Div([
    html.H1('Olympic Medals Count by Country', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='dropdown-country',
        options=[{'label': i, 'value': i} for i in df['Country Code'].unique()],
        value=df['Country Code'].unique(),  # Default to all countries
        multi=True,  # Allow multiple selections
        clearable=False
    ),
    dcc.Graph(id="medals-count")
])

@callback(
    Output('medals-count', 'figure'),
    Input('dropdown-country', 'value')
)
def update_graph(selected_countries):
    if not selected_countries:
        # If no countries are selected, display data for all countries
        filtered_df = df
    else:
        # Filter the dataframe for selected countries
        filtered_df = df[df['Country Code'].isin(selected_countries)]

    # Count the medals by type and prepare data for plotting
    medal_counts = filtered_df.groupby(['Medal Type']).size().reset_index(name='Count')
    medal_counts = medal_counts.sort_values('Medal Type', ascending=False)  # Sort to maintain color consistency

    # Define custom colors for medal types
    colors = {'Bronze Medal': 'red', 'Silver Medal': 'blue', 'Gold Medal': 'green'}

    # Create the figure
    fig = px.bar(
        medal_counts, 
        x='Medal Type', 
        y='Count', 
        color='Medal Type',
        color_discrete_map=colors,
        title='Medals Distribution'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
