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
        options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Country Code'].unique()],
        value='All',  # Default to 'All'
        multi=True,  # Allow multiple selections
        clearable=False,
        placeholder="Choose a Country"  # Updated placeholder text
    ),
    dcc.Dropdown(
        id='dropdown-sport',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': s, 'value': s} for s in df['Sport Discipline'].dropna().unique()],
        value='All',  # Default to 'All'
        multi=False,
        clearable=False,
        placeholder="Choose a Sport"  # Updated placeholder text for sport
    ),
    dcc.Graph(id="medals-count")
])

@callback(
    Output('medals-count', 'figure'),
    Input('dropdown-country', 'value'),
    Input('dropdown-sport', 'value')
)
def update_graph(selected_countries, selected_sport):
    if 'All' in selected_countries or not selected_countries:
        filtered_df = df
    else:
        filtered_df = df[df['Country Code'].isin(selected_countries)]
    
    if selected_sport != 'All':
        filtered_df = filtered_df[filtered_df['Sport Discipline'] == selected_sport]
    
    medal_counts = filtered_df.groupby(['Country Code', 'Medal Type']).size().reset_index(name='Count')
    fig = px.bar(medal_counts, x='Country Code', y='Count', color='Medal Type',
                 title='Medals Distribution', barmode='group',
                 color_discrete_map={'Gold Medal': 'red', 'Silver Medal': 'blue', 'Bronze Medal': 'green'})
    fig.update_layout(legend_title_text='Medal Type',
                      legend=dict(title_font_family='Arial'))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
