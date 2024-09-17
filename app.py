from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Visualization"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

app.layout = html.Div([
    html.H1('Olympic Medals Count by Gender', style={'textAlign': 'center'}),
    dcc.Graph(id="medals-gender")
])

@app.callback(
    Output('medals-gender', 'figure'),
    Input('medals-gender', 'id')  # Dummy input for initialization
)
def update_graph(_):
    fig = px.scatter(df, x="Medal Type", y="Medal Date",
                     color="Medal Type", facet_col="Gender",
                     hover_data=["Athlete Name", "Country Code", "Sport Discipline"])
    fig.update_traces(marker=dict(size=10))  # Adjust marker size for visibility
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
