from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympics 2024"
server = app.server

df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Unique sports for the dropdown
sports = df['Sport Discipline'].unique()
sports_options = [{'label': 'All', 'value': 'All'}] + [{'label': sport, 'value': sport} for sport in sports]

app.layout = html.Div([
    html.H1("Olympic Medals by Country and Sport", style={'textAlign': 'center'}),
    
    # Sport dropdown
    dcc.Dropdown(
        id='sport-dropdown',
        options=sports_options,
        value=['All'],  # Default value is 'All'
        clearable=False,
        multi=True,
        style={'width': '50%', 'margin': '10px auto'},
        placeholder="Choose a sport"
    ),
    
    # Stacked bar chart
    dcc.Graph(id='medals-stacked-bar'),
    
    # Sunburst chart
    html.H2("Sunburst Chart: Countries → Sports → Athletes → Medals", style={'textAlign': 'center'}),
    dcc.Graph(id='medals-sunburst')
])

# Callback to update both figures
@app.callback(
    [Output('medals-stacked-bar', 'figure'),
     Output('medals-sunburst', 'figure')],
    [Input('sport-dropdown', 'value')]
)
def update_charts(selected_sports):
    # Filter by selected sports
    if 'All' in selected_sports or not selected_sports:
        filtered_df = df
    else:
        filtered_df = df[df['Sport Discipline'].isin(selected_sports)]
    
    # Stacked bar chart
    bar_data = filtered_df.groupby(['Country Code', 'Medal Type']).size().reset_index(name='Counts')
    bar_data = bar_data.pivot(index='Country Code', columns='Medal Type', values='Counts').fillna(0)
    
    fig1 = px.bar(bar_data, x=bar_data.index, y=['Gold Medal', 'Silver Medal', 'Bronze Medal'],
                  title="Medal Counts by Country",
                  labels={'value': 'Number of Medals', 'Country Code': 'Country'},
                  color_discrete_map={'Gold Medal': 'gold', 'Silver Medal': 'silver', 'Bronze Medal': '#cd7f32'})
    fig1.update_layout(barmode='stack')
    
    # Sunburst chart: Countries → Sports → Athletes → Medals
    fig2 = px.sunburst(filtered_df, 
                       path=['Country Code', 'Sport Discipline', 'Athlete Name', 'Medal Type'], 
                       values=None,
                       color='Medal Type',
                       color_discrete_map={'Gold Medal': 'gold', 'Silver Medal': 'silver', 'Bronze Medal': '#cd7f32'},
                       title="Sunburst: Countries → Sports → Athletes → Medals")
    
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
