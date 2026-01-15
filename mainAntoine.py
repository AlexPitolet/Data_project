import numpy as np
import plotly_express as px 
import geojson
import pandas as pd
import geopandas
import folium
import branca.colormap as cm 
from typing import Literal
import os







def select_data(data,level:Literal["commune","departement","region"],year):
    data = data.query(f"Année=={year}")
    data_dir = "data/cleaned"

    if level == "commune":
        col_name = 'Code Commune'
        geojson = os.path.join(data_dir,"communes_france.geojson")

    elif level == "departement":
        col_name = 'Code Département'
        geojson = os.path.join(data_dir,"departements.geojson")
        data = data.groupby(col_name,as_index=False)["Conso totale (MWh)"].sum()

    elif level == "region":
        col_name = 'Code Région'
        geojson = os.path.join(data_dir,"regions.geojson")
        data = data.groupby(col_name,as_index=False)["Conso totale (MWh)"].sum()

    else:
        print(f"Erreur de level : {level}")
        return

    return data, geojson, col_name

def create_map(data,geojson,col_name,year):

    min = data["Conso totale (MWh)"].min()
    max = data["Conso totale (MWh)"].max()

    coords = (48.7190835,2.4609723)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

    colormap = cm.linear.YlGn_09.scale(min, max)
    colormap.caption = "Consommation totale (MWh)"
    colormap.add_to(map)

    folium.Choropleth(
        geo_data=geojson,
        name=f"Map of total electricity consumption (MWh) in {str(year)}",
        data=data,
        columns=[col_name,'Conso_log'],
        key_on='feature.properties.code_commune',
        fill_color='YlGn',
        fill_opacity='0.7',
        line_opacity=0.2,
        overlay=False,
        legend_name="Conso totale log",
        show=(year==2023)
    ).add_to(map)

    map.save(outfile='map.html')
    return map

def create_maps(df,years,level):
    for year in years:
        data, geojson, col_name = select_data(df,level,year)
        
        min = data["Conso totale (MWh)"].min()
        max = data["Conso totale (MWh)"].max()

        coords = (48.7190835,2.4609723)
        map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

        colormap = cm.linear.YlGn_09.scale(min, max)
        colormap.caption = "Consommation totale (MWh)"
        colormap.add_to(map)

        folium.Choropleth(
            geo_data=geojson,
            name=f"Map of total electricity consumption (MWh) in {str(year)}",
            data=data,
            columns=[col_name,'Conso_log'],
            key_on='feature.properties.code_commune',
            fill_color='YlGn',
            fill_opacity='0.7',
            line_opacity=0.2,
            overlay=False,
            legend_name="Conso totale log",
            show=(year==2023)
        ).add_to(map)

        map.save(outfile='map.html')
        return map

    map.save(outfile='map.html')


def main():
    data_dir          = "data\\raw\\consommation-annuelle-d-electricite-et-gaz-par-commune.csv"
    df                = pd.read_csv("data\\raw\\consommation-annuelle-d-electricite-et-gaz-par-commune.csv",sep=";")
    code_villes       = df["Code Commune"]
    code_departements = df["Code Département"].unique()
    code_regions      = df["Code Région"].unique()
    years        = df["Année"].unique()
    

    ### IDF 
    idf_codes = ('75','77','78','91','92','93','94','95')
    mask = df["Code Commune"].fillna("").astype(str).str.startswith(idf_codes)

    idf_data = df[mask]
    idf_data["Conso_log"] = np.log1p(idf_data["Conso totale (MWh)"])

    ### FRANCE 
    df["Conso_log"] = np.log1p(df["Conso totale (MWh)"])

    
    


    #with open("map.html",'r') as f: 
    #    html_data = f.read()

if __name__=="__main__":
    #main()
    df1 = pd.read_csv("data/raw/consommation-annuelle-d-electricite-et-gaz-par-commune.csv",sep=';')
    df1.info()
    #df2 = pd.read_csv("consommation-annuelle-d-electricite-et-gaz-par-commune.csv",sep=';')
    #print(df2.info())