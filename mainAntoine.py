import numpy as np
import plotly_express as px 
import geojson
import pandas as pd
import geopandas
import folium
import branca.colormap as cm 
import plotly.express as px
from typing import Literal
import os
import json

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


def select_data(data,level:Literal["commune","departement","region"],year):
    data = data.query(f"Année=={year}")
    data_dir = "data/cleaned"

    if level == "commune":
        col_name = 'Code Commune'
        geojson_path = os.path.join(data_dir,"communes_france.geojson")
        with open(geojson_path) as f:
            geojson = json.load(f)
        key_on = 'properties.code_commune'

    elif level == "departement":
        col_name = 'Code Département'
        geojson_path = os.path.join(data_dir,"departements.geojson")
        with open(geojson_path) as f:
            geojson = json.load(f)
        data = data.groupby(col_name,as_index=False)["Conso totale (MWh)"].sum()
        key_on = 'properties.code'

    elif level == "region":
        col_name = 'Code Région'
        geojson_path = os.path.join(data_dir,"regions.geojson")
        with open(geojson_path) as f:
            geojson = json.load(f)
        data = data.groupby(col_name,as_index=False)["Conso totale (MWh)"].sum()
        key_on = 'properties.code'

    else:
        print(f"Erreur de level : {level}")
        return

    return data, geojson, col_name, key_on

def create_map(map,data,geojson,col_name,year,key_on):
    min = data["Conso totale (MWh)"].min()
    max = data["Conso totale (MWh)"].max()

    colormap = cm.linear.YlGn_09.scale(min, max)
    colormap.caption = "Consommation totale (MWh)"
    #colormap.add_to(map)

    folium.Choropleth(
            geo_data=geojson,
            name=f"Map of total electricity consumption (MWh) in {str(year)}",
            data=data,
            columns=[col_name,'Conso totale (MWh)'],
            key_on=key_on,
            fill_color='YlGn',
            fill_opacity='0.7',
            line_opacity=0.2,
            overlay=False,
            legend_name="Consommation totale (MWh)",
            show=(year==2023)
        ).add_to(map)
    

def create_maps(df,years,level):
    coords = (48.7190835,2.4609723)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)

    for year in years:
        print(f"Map {year} generating")
        data, geojson, col_name, key_on = select_data(df,level,year)
        
        min = data["Conso totale (MWh)"].min()
        max = data["Conso totale (MWh)"].max()

        colormap = cm.linear.YlGn_09.scale(min, max)
        colormap.caption = "Consommation totale (MWh)"
        #colormap.add_to(map)
        create_map(map,data,geojson,col_name,year,key_on)
        
    folium.LayerControl(collapsed=False).add_to(map)
    map.save(outfile='map.html')


def main():
    data_dir            = "data\\cleaned\\codes_et_conso_totale.csv"
    df                  = pd.read_csv(data_dir)
    years               =  df["Année"].unique()
    year = years.min() #2011
    level = "region"

    

    app = Dash(__name__)
    
    data, geojson, col_name, key_on = select_data(df,level,year)
    
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


    app.layout = html.Div([ 
                        html.Label('Year'),
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
                            value=year,
                        ),
                        html.Label('Scale'),
                        dcc.Dropdown(
                            id="scale-dropdown",
                            options=[
                                {'label': 'Commune', 'value': "commune"},
                                {'label': 'Département', 'value': "departement"},
                                {'label': 'Région', 'value': "region"},
                            ],
                            value=level,
                        ),

                        html.H1(id='H1',
                                children=f"Map de la consommation d'électricité totale entre {year}",        
                                style={'textAlign': 'center', 'color': '#7FDBFF'}),
                        dcc.Graph(
                                id='map',
                                figure=fig,
                                style={"height": "80vh"}
                            ), # (6)

                        html.Div(id="desc",
                                 children=f'''
                            The graph above shows relationship between life expectancy and
                            GDP per capita for year {year}. Each continent data has its own
                            colour and symbol size is proportionnal to country population.
                            Mouse over for details.
                        '''), # (7)
        ])
    
    @app.callback(
        Output(component_id='map', component_property='figure'), # (1)
        Output(component_id='H1', component_property='children'),
        Output(component_id="desc",component_property='children'),
        [Input(component_id='year-dropdown', component_property='value'),
         Input(component_id='scale-dropdown', component_property='value')] # (2)
    )
    def update_figure(year, scale): # (3)
        data, geojson, col_name, key_on = select_data(df,scale,year)
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
    #create_maps(df,years,"region")
    app.run(debug=True)
    

if __name__=="__main__":
    pass
    
    
















    ### IDF 
    #idf_codes = ('75','77','78','91','92','93','94','95')
    #mask = df["Code Commune"].fillna("").astype(str).str.startswith(idf_codes)
    #idf_data = df[mask]

    ### FRANCE 
    #df["Conso_log"] = np.log1p(df["Conso totale (MWh)"])