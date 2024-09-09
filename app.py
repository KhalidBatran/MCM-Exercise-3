from dash import Dash, html, dcc
import numpy as np 
import pandas as pd 
import plotly.express as px

app = Dash(__name__)
app.title = "MCM7183 Exercise 3"
server = app.server

df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Exercise-3/main/assets/gdp_1960_2020.csv")



image_path = 'assets/logo-mmu.png'

app.layout = [html.H1('MCM7183 Exercise 3'), 
              html.Img(src=image_path), 
              dcc.Dropdown(['Malaysia', 'Indonesia', 'China'], 'Malaysia', id='dropdown-country'),
              dcc.Graph(id="graph-scatter"), 
              dcc.Dropdown(['2020', '2010', '2000'], '2020', id='dropdown-year'),
              dcc.Graph(id="graph-pie")]

@callback(
    Output('graph-scatter', 'figure'),
    Output('graph-pie', 'figure'),
    Input('dropdown-country', 'value'),
    Input('dropdown-year', 'value'),
)
def update_graph(country_selected, year_selected):
    subset_Country = df[df['country'].isin([country_selected])]
    fig = px.scatter(subset_Country, x="year", y="gdp")

    subset_Year = df[df['year'].isin([year_selected])]
    subset_Year_Asia = subset_Year[subset_Year['state'].isin(["Asia"])]
    subset_Year_Africa = subset_Year[subset_Year['state'].isin(["Africa"])]
    subset_Year_America = subset_Year[subset_Year['state'].isin(["America"])]
    subset_Year_Europe = subset_Year[subset_Year['state'].isin(["Europe"])]
    subset_Year_Oceania = subset_Year[subset_Year['state'].isin(["Oceania"])]
    pie_data = [sum(subset_Year_Asia['gdp']),sum(subset_Year_Africa['gdp']),sum(subset_Year_America['gdp']),sum(subset_Year_Europe['gdp']),sum(subset_Year_Oceania['gdp'])];
    mylabels = ["Asia", "Africa", "America", "Europe","Oceania"]
    pie_df = {'Continent': mylabels,'GDP': pie_data}
    fig2 = px.pie(pie_df,values="GDP",names="Continent")

    return fig, fig2


if __name__ == '__main__':
    app.run(debug=True)
