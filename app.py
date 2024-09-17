from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Stacked Bar Chart"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Unique sports for dropdown
sports = df['Sport Discipline'].unique()

app.layout = html.Div([
    html.H1("Olympic Medals by Country and Sport", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='sport-dropdown',
        options=[{'label': sport, 'value': sport} for sport in sports],
        value=sports[0],  # Default to the first sport available
        clearable=False,
        style={'width': '50%', 'margin': '10px auto'}
    ),
    dcc.Graph(id='medals-stacked-bar')
])

@app.callback(
    Output('medals-stacked-bar', 'figure'),
    Input('sport-dropdown', 'value')
)
def update_stacked_bar(selected_sport):
    # Filter data based on the selected sport
    filtered_df = df[df['Sport Discipline'] == selected_sport]
    
    # Prepare data for the stacked bar chart
    bar_data = filtered_df.groupby(['Country Code', 'Medal Type']).size().reset_index(name='Counts')
    bar_data = bar_data.pivot(index='Country Code', columns='Medal Type', values='Counts').fillna(0)
    
    # Create the stacked bar chart
    fig = px.bar(bar_data, x=bar_data.index, y=['Gold Medal', 'Silver Medal', 'Bronze Medal'],
                 title=f"Medal Counts by Country for {selected_sport}",
                 labels={'value': 'Number of Medals', 'Country Code': 'Country'},
                 color_discrete_map={'Gold Medal': 'gold', 'Silver Medal': 'silver', 'Bronze Medal': '#cd7f32'})
    fig.update_layout(barmode='stack')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
