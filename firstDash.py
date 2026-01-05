
#
# Imports
#
import numpy as np
import pandas as pd
import plotly.express as px

import dash
from dash import Dash,dcc,html
from dash.dependencies import Input,Output

#
# Data
#

df = pd.read_csv("data/raw/dataset/global_air_quality_data_10000.csv")
df["Date"] = pd.to_datetime(df["Date"])

countries =[]
for country,i in enumerate(df["Country"].unique()) : 
    countries[i] = country

print(countries)

#
# Main
#

def main():
    app = dash.Dash(__name__) # (3)

    fig = px.bar(df, x="Country", y="Temperature", color="Country") # (4)


    app.layout = html.Div(children=[

                            html.H1(children=f'Temperature per country ',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                            html.Div(children=f'''
                                The graph above shows relationship between temperature and
                                country. Each country data has its own
                                bar and size is proportionnal to country mean temperature.
                                Mouse over for details.
                            '''), # (7)

    ]
    )

    #
    # RUN APP
    #

    app.run(debug=True) # (8)

if __name__ == '__main__':
    main()