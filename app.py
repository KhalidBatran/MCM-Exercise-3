from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from pandas.api.types import CategoricalDtype

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Visualization"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Define medal order
medal_order = CategoricalDtype(['Gold Medal', 'Silver Medal', 'Bronze Medal'], ordered=True)
df['Medal Type'] = df['Medal Type'].astype(medal_order)

app.layout = html.Div([
    html.H1('Olympic Medals Count by Country', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='dropdown-country',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Country Code'].unique()],
        value='All',  # Default value to show all countries
        clearable=False,
        multi=True
    ),
    dcc.Graph(id="medals-count")
])

@callback(
    Output('medals-count', 'figure'),
    Input('dropdown-country', 'value')
)
def update_graph(selected_countries):
    if 'All' in selected_countries or not selected_countries:
        filtered_df = df
    else:
        filtered_df = df[df['Country Code'].isin(selected_countries)]
    medal_counts = filtered_df['Medal Type'].value_counts().reset_index()
    medal_counts.columns = ['Medal Type', 'Count']
    fig = px.bar(medal_counts, x='Country Code', y='Count', color='Medal Type',
                 title='Medals Distribution', barmode='group',
                 color_discrete_map={'Gold Medal': 'red', 'Silver Medal': 'blue', 'Bronze Medal': 'green'})
    fig.update_layout(legend_title_text='Medal Type',
                      legend=dict(title_font_family='Arial', itemsizing='constant', traceorder='normal'))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
