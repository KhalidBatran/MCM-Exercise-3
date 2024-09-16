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
        value='USA',  # Default value
        clearable=False
    ),
    dcc.Graph(id="medals-count")
])

@callback(
    Output('medals-count', 'figure'),
    Input('dropdown-country', 'value')
)
def update_graph(selected_country):
    filtered_df = df[df['Country Code'] == selected_country]
    medal_counts = filtered_df['Medal Type'].value_counts().reset_index()
    medal_counts.columns = ['Medal Type', 'Count']
    fig = px.bar(medal_counts, x='Medal Type', y='Count', color='Medal Type',
                 title=f"Medals Distribution for {selected_country}")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
