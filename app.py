import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

# Initialize the Dash app with external stylesheets for better styling.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

# Load the cleaned dataset from a public URL.
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/Olympics%202024.csv")

# Parse 'Medal Date' to datetime and drop any rows with errors in date parsing.
df['Medal Date'] = pd.to_datetime(df['Medal Date'], errors='coerce', format='%d-%b')
df = df.dropna(subset=['Medal Date'])
df['Day Month'] = df['Medal Date'].dt.strftime('%d %b')

# Define sidebar style for navigation.
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "transition": "0.3s"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "transition": "0.3s",
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Olympics Bar Chart", href="/fig1", active="exact"),
                dbc.NavLink("Olympics Line Progression", href="/fig2", active="exact"),
                dbc.NavLink("Olympics Gender Comparison", href="/fig3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Button to toggle the sidebar for better responsiveness.
sidebar_toggle_button = dbc.Button("Toggle Sidebar", id="toggle-button", n_clicks=0, style={"margin": "10px"})

# Main layout of the app including sidebar and content layout.
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar_toggle_button,
    sidebar,
    html.Div(id="page-content", style=CONTENT_STYLE)
])

# Home page layout.
def home_layout():
    return html.Div(
        style={"textAlign": "center"},
        children=[
            html.H1("The Olympic Medals Visualization", style={'font-weight': 'bold', 'margin-bottom': '20px'}),
            html.P("Welcome to the Olympic Medals Dashboard! Explore data from the Olympic Games."),
            html.Br(),
            html.H2("Navigate through the dashboard using the sidebar to see detailed visualizations.")
        ]
    )

# Callback to dynamically load the correct page based on URL.
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return home_layout()
    elif pathname == "/fig1":
        return fig1_layout()
    elif pathname == "/fig2":
        return fig2_layout()
    elif pathname == "/fig3":
        return fig3_layout()
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

# Figure 1 layout and callback
def fig1_layout():
    medal_data = df.groupby(['Country Code', 'Medal Type']).size().reset_index(name='Count')
    fig = px.bar(medal_data, x='Country Code', y='Count', color='Medal Type',
                 color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'},
                 labels={'Count': 'Medals Count'},
                 title='Medals Count by Country and Type')
    return html.Div([
        html.H1('Olympics Medals by Country', style={'textAlign': 'center'}),
        dcc.Graph(figure=fig)
    ])

# Figure 2 layout and callback
def fig2_layout():
    filtered_df = df if not df.empty else df
    fig = px.line(filtered_df, x='Day Month', y='Country Code', color='Athlete Name',
                  title='Athlete Medal Progression Over Time')
    return html.Div([
        html.H1('Athlete Medal Progression', style={'textAlign': 'center'}),
        dcc.Graph(figure=fig)
    ])

# ... previous code ...

# Figure 3 layout and callback
def fig3_layout():
    gender_medals = df.groupby(['Medal Type', 'Gender']).size().reset_index(name='Total')
    fig = px.bar(gender_medals, x='Medal Type', y='Total', color='Gender',
                 color_discrete_map={'M': 'blue', 'F': 'pink'},
                 barmode='group',
                 title='Medal Comparison by Gender')
    fig.update_traces(hovertemplate="<b>Medal:</b> %{x}<br><b>Gender:</b> %{color}<br><b>Total:</b> %{y}<extra></extra>")
    return html.Div([
        html.H1('Comparison of Medals by Gender', style={'textAlign': 'center'}),
        dcc.Graph(figure=fig)
    ])

# Callback functions for dynamic content loading based on navigation
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return home_layout()
    elif pathname == "/fig1":
        return fig1_layout()
    elif pathname == "/fig2":
        return fig2_layout()
    elif pathname == "/fig3":
        return fig3_layout()
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
