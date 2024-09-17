from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Heatmap"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Assuming 'Medal Date' contains date information and you want to focus on years
df['Year'] = pd.to_datetime(df['Medal Date']).dt.year
years = df['Year'].unique()

app.layout = html.Div([
    html.H1("Olympic Medals Count by Country and Sport", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in sorted(years)],
        value=years[0],  # Default to the first year available
        clearable=False,
        style={'width': '50%', 'margin': '10px auto'}
    ),
    dcc.Graph(id='medals-heatmap')
])

@app.callback(
    Output('medals-heatmap', 'figure'),
    Input('year-dropdown', 'value')
)
def update_heatmap(selected_year):
    # Filter data based on the selected year
    filtered_df = df[df['Year'] == selected_year]
    
    # Prepare the data for the heatmap
    heatmap_data = filtered_df.groupby(['Country Code', 'Sport Discipline']).size().unstack(fill_value=0)
    
    # Create the heatmap
    fig = px.imshow(heatmap_data, labels=dict(x="Sport Discipline", y="Country", color="Medal Count"),
                    aspect="auto", title=f"Medal Distribution for {selected_year}")
    fig.update_xaxes(side="bottom")
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
