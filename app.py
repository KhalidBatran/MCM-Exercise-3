from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Visualization"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")
print(df.columns)  # Print the columns to verify if 'Sport' is present

# Define the layout of the app
app.layout = html.Div([
    html.H1('Olympic Medals Count by Country and Sport', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='dropdown-country',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Country Code'].unique()],
        value='All',  # Default to 'All'
        multi=True,  # Allow multiple selections
        clearable=False
    ),
    dcc.Dropdown(
        id='dropdown-sport',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in df.get('Sport', ['All']).unique()],
        value='All',  # Default to 'All'
        multi=True,  # Allow multiple selections
        clearable=False
    ),
    dcc.Graph(id="medals-count")
])

# Define the callback to update the graph
@callback(
    Output('medals-count', 'figure'),
    Input('dropdown-country', 'value'),
    Input('dropdown-sport', 'value')
)
def update_graph(selected_countries, selected_sports):
    if 'All' in selected_countries or not selected_countries:
        filtered_df = df
    else:
        filtered_df = df[df['Country Code'].isin(selected_countries)]
    
    if 'All' not in selected_sports and 'Sport' in df.columns:
        filtered_df = filtered_df[filtered_df['Sport'].isin(selected_sports)]

    medal_counts = filtered_df.groupby(['Country Code', 'Medal Type']).size().reset_index(name='Count')
    fig = px.bar(medal_counts, x='Country Code', y='Count', color='Medal Type',
                 title='Medals Distribution by Sport and Country', barmode='group',
                 color_discrete_map={'Gold Medal': 'red', 'Silver Medal': 'blue', 'Bronze Medal': 'green'})
    fig.update_layout(legend_title_text='Medal Type',
                      legend=dict(title_font_family='Arial'))
    return fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
