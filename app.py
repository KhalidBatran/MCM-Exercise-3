from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Bubble Chart"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Group data to count medals by type, country, and sport
medal_counts = df.groupby(['Country Code', 'Sport Discipline', 'Medal Type']).size().reset_index(name='Counts')

app.layout = html.Div([
    html.H1("Olympic Medals Distribution by Country and Sport", style={'textAlign': 'center'}),
    dcc.Graph(id='medals-bubble-chart')
])

@app.callback(
    Output('medals-bubble-chart', 'figure'),
    Input('medals-bubble-chart', 'id')  # Dummy input for initialization
)
def update_bubble_chart(_):
    fig = px.scatter(medal_counts, x="Sport Discipline", y="Country Code",
                     size="Counts", color="Medal Type",
                     hover_name="Country Code", size_max=60,
                     title="Medal Counts by Country and Sport Discipline")
    fig.update_layout(xaxis_title="Sport Discipline", yaxis_title="Country")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
