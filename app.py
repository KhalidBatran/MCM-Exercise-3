from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv')

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Medals Count by Country", className='text-center mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='filter-country', 
                         options=[{'label': country, 'value': country} for country in df['Country Code'].unique()],
                         value=[], 
                         multi=True, 
                         placeholder="Select Country(s)")
        ], width=4),
        dbc.Col([
            dcc.Dropdown(id='filter-gender', 
                         options=[{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
                         value='All', 
                         multi=False, 
                         placeholder="Select Gender")
        ], width=4),
        dbc.Col([
            dcc.Dropdown(id='filter-medal', 
                         options=[{'label': medal, 'value': medal} for medal in df['Medal Type'].unique()],
                         value=[], 
                         multi=True, 
                         placeholder="Select Medal Type(s)")
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='medals-graph'), width=12)
    ])
])

@callback(
    Output('medals-graph', 'figure'),
    [Input('filter-country', 'value'),
     Input('filter-gender', 'value'),
     Input('filter-medal', 'value')]
)
def update_graph(selected_countries, selected_gender, selected_medals):
    filtered_df = df.copy()

    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country Code'].isin(selected_countries)]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    if selected_medals:
        filtered_df = filtered_df[filtered_df['Medal Type'].isin(selected_medals)]

    # Check if the dataframe is empty
    if filtered_df.empty:
        print("Filtered dataframe is empty after applying filters.")
    else:
        print("Filtered dataframe has data.")

    # Aggregate data by country and medal type
    medal_counts = filtered_df.groupby(['Country Code', 'Medal Type']).size().unstack(fill_value=0)

    # Debug output
    print("Medal counts dataframe:")
    print(medal_counts)

    fig = go.Figure(
        data=[
            go.Bar(name='Gold', x=medal_counts.index, y=medal_counts.get('Gold', []), marker_color='gold'),
            go.Bar(name='Silver', x=medal_counts.index, y=medal_counts.get('Silver', []), marker_color='silver'),
            go.Bar(name='Bronze', x=medal_counts.index, y=medal_counts.get('Bronze', []), marker_color='brown')
        ]
    )

    fig.update_layout(barmode='stack', title="Medals Count by Country")

    if fig.data:
        print("Graph has data.")
    else:
        print("Graph is empty.")

    return fig

if __name__ == '__main__':
    app.run(debug=True)
