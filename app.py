from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.title = "Olympic Medals Heatmap"
server = app.server

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/cleaned_medals.csv")

# Format 'Medal Date' to show day and month
df['Formatted Date'] = pd.to_datetime(df['Medal Date']).dt.strftime('%d %b')  # Example: '27 Jul'

dates = df['Formatted Date'].unique()

app.layout = html.Div([
    html.H1("Olympic Medals Count by Country and Sport", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='date-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': date, 'value': date} for date in sorted(dates)],
        value='All',  # Default to 'All'
        clearable=False,
        style={'width': '50%', 'margin': '10px auto'}
    ),
    dcc.Graph(id='medals-heatmap')
])

@app.callback(
    Output('medals-heatmap', 'figure'),
    Input('date-dropdown', 'value')
)
def update_heatmap(selected_date):
    # Filter data based on the selected date or show all
    if selected_date == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Formatted Date'] == selected_date]
    
    # Prepare the data for the heatmap
    heatmap_data = filtered_df.groupby(['Country Code', 'Sport Discipline']).size().unstack(fill_value=0)
    
    # Create the heatmap
    fig = px.imshow(heatmap_data, labels=dict(x="Sport Discipline", y="Country", color="Medal Count"),
                    aspect="auto", title=f"Medal Distribution for {selected_date}")
    fig.update_xaxes(side="bottom")
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
