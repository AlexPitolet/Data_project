from dash import html, dcc, Input, Output
import pandas as pd
import plotly_express as px
from src.utils.common_fuctions import select_data

level = "region"
year = 2011

data, geojson, col_name, key_on = select_data(level,year)

fig = px.choropleth_map(
        data_frame=data,
        geojson=geojson,
        locations=col_name,
        featureidkey=key_on,
        color="Conso totale (MWh)",
        color_continuous_scale="YlGn",
        center={"lat": 46.6, "lon": 2.5},  # centre de la France
        zoom=5
    )

layout = html.Div([ 
                        html.H1(id='H1',
                            children=f"Map de la consommation d'électricité totale entre {year}",        
                            style={
                                'textAlign': 'center', 
                                'color': '#7FDBFF',
                            }
                        ),
                        html.Div([
                            html.Div([
                                html.Label('Année'),
                                dcc.Dropdown(
                                    id="year-dropdown",
                                    options=[
                                        {'label': '2011', 'value': 2011},
                                        {'label': '2012', 'value': 2012},
                                        {'label': '2013', 'value': 2013},
                                        {'label': '2014', 'value': 2014},
                                        {'label': '2015', 'value': 2015},
                                        {'label': '2016', 'value': 2016},
                                        {'label': '2017', 'value': 2017},
                                        {'label': '2018', 'value': 2018},
                                        {'label': '2019', 'value': 2019},
                                        {'label': '2020', 'value': 2020},
                                        {'label': '2021', 'value': 2021},
                                        {'label': '2022', 'value': 2022},
                                        {'label': '2023', 'value': 2023},
                                        {'label': '2024', 'value': 2024},
                                    ],
                                    value=2011,
                                ),
                                html.Label('Échelle'),
                                dcc.Dropdown(
                                    id="scale-dropdown",
                                    options=[
                                        #{'label': 'Commune', 'value': "commune"},
                                        {'label': 'Département', 'value': "departement"},
                                        {'label': 'Région', 'value': "region"},
                                    ],
                                    value="region",
                                )
                                ],
                                style={
                                    "display":"flex",
                                    "flexDirection":"column",
                                    "witdh":"40vw",
                                }),
                                dcc.Graph(
                                    id='map',
                                    figure=fig,
                                    style={"height": "80vh","width":"60vw"}
                                )
                            ],
                            style={
                                "display":"flex",
                                "alignItems":"center",
                                "justifyContent":"center"
                            }
                            ),
                        
                        html.Div(id="desc",
                                 children=f'''
                            The graph above shows relationship between life expectancy and
                            GDP per capita for year 2011. Each continent data has its own
                            colour and symbol size is proportionnal to country population.
                            Mouse over for details.
                        ''')
        ])
    
def register_callback(app):
    @app.callback(
        Output(component_id='map', component_property='figure'), 
        Output(component_id='H1', component_property='children'),
        Output(component_id="desc",component_property='children'),
        [Input(component_id='year-dropdown', component_property='value'),
         Input(component_id='scale-dropdown', component_property='value')] # (2)
    )
    def update_figure(year, scale): # (3)
        data, geojson, col_name, key_on = select_data(scale,year)
        fig = px.choropleth_map(
            data_frame=data,
            geojson=geojson,
            featureidkey=key_on,
            locations=col_name,
            color="Conso totale (MWh)",
            color_continuous_scale="YlGn",
            center={"lat": 46.6, "lon": 2.5},  # centre de la France
            zoom=5
            ) # (4)
        title = f"Map de la consommation d'électricité totale entre {year} au niveau {scale}"
        desc = f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year {year}. Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            '''
        return fig,title,desc