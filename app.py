import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Format the 'Medal Date' for display
df['Medal Date'] = pd.to_datetime(df['Medal Date']).dt.strftime('%d %B')

app.layout = html.Div([
    html.H1("Comparison of Genders and Medals", style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + 
                [{'label': country, 'value': country} for country in df['Country Code'].unique()],
        value='All',
        clearable=False,
        multi=True,  # Correct boolean value for multi-select
        style={'width': '50%', 'margin': '10px auto'},
        placeholder="Choose country or countries"
    ),
    
    dcc.Graph(id='gender-medal-bar-chart')
])

@app.callback(
    Output('gender-medal-bar-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_gender_medal_chart(selected_countries):
    # Filter the dataframe based on the selected country or countries
    if 'All' in selected_countries or not selected_countries:
        filtered_df = df
    else:
        filtered_df = df[df['Country Code'].isin(selected_countries)]

    # Create a bar chart
    fig = px.bar(
        filtered_df,
        x='Medal Type',
        y='count',  # Aggregating the count for medals
        color='Gender',
        barmode='group',
        title="Comparison of Genders and Medals",
        labels={'Medal Type': 'Medal Type', 'count': 'Number of Medals'},
        color_discrete_map={'M': 'blue', 'F': 'pink'}
    )

    # Customize the hover data
    fig.update_traces(
        hovertemplate=(
            '<b>Athlete Name:</b> %{customdata[0]}<br>' +
            '<b>Medal Date:</b> %{customdata[1]}<br>' +
            '<b>Sport Discipline:</b> %{customdata[2]}<br>' +
            '<b>Country:</b> %{customdata[3]}<br>'
        ),
        customdata=filtered_df[['Athlete Name', 'Medal Date', 'Sport Discipline', 'Country Code']].values
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
