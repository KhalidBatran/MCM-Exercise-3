from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv')

# Aggregate data by country and medal type
medal_counts = df.groupby('Country Code')['Medal Type'].value_counts().unstack().fillna(0)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Medals Count by Country", className='text-center mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='medals-graph'), width=12)
    ])
])

@app.callback(
    Output('medals-graph', 'figure'),
    Input('medals-graph', 'id')  # This input is just to initialize the graph
)
def update_graph(_):
    fig = go.Figure()
    if not medal_counts.empty:
        fig.add_trace(go.Bar(name='Gold', x=medal_counts.index, y=medal_counts.get('Gold', []), marker_color='gold'))
        fig.add_trace(go.Bar(name='Silver', x=medal_counts.index, y=medal_counts.get('Silver', []), marker_color='silver'))
        fig.add_trace(go.Bar(name='Bronze', x=medal_counts.index, y=medal_counts.get('Bronze', []), marker_color='brown'))
        fig.update_layout(barmode='stack', title="Medals Count by Country")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
