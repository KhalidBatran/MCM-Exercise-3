from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Visualization by Gender"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Create a pivot table or aggregate data as needed for the scatter plot
medal_counts = df.groupby(['Gender', 'Medal Type']).size().reset_index(name='Count')

# Plotting the scatter plot
fig = px.scatter(medal_counts, x="Medal Type", y="Count",
                color="Medal Type", facet_col="Gender", hover_data=["Gender", "Medal Type"])

app.layout = html.Div([
    html.H1('Olympic Medals Count by Gender', style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
