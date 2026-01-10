import numpy as np
import plotly_express as px 
import geojson
import pandas as pd
import geopandas
import folium
import branca.colormap as cm 

def createMap(data,geojson,level,year):
    
    min = data["Conso totale (MWh)"].min()
    max = data["Conso totale (MWh)"].max()

    coords = (48.7190835,2.4609723)
    map1 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

    colormap = cm.linear.YlGn_09.scale(min, max)
    colormap.caption = "Consommation totale (MWh)"
    colormap.add_to(map1)

    folium.Choropleth(
        geo_data=geojson,
        name="Consommation d'électricité en France en 2023",
        data=data,
        columns=['Code Commune','Conso_log'],
        key_on='feature.properties.code_commune',
        fill_color='YlGn',
        fill_opacity='0.7',
        line_opacity=0.2,
        overlay=False,
        legend_name="Conso totale log"
    ).add_to(map1)

    map1.save(outfile='map.html')


def main():
    data_dir = "data\\raw\\consommation-annuelle-d-electricite-et-gaz-par-commune.csv"
    df           = pd.read_csv(data_dir,sep=';')
    code_villes       = df["Code Commune"]
    code_departements = df["Code Département"].unique()
    code_regions      = df["Code Région"].unique()
    years        = df["Année"].unique()
    france_data    = df.query("Année==2023")
    print(code_departements)
    print(code_regions)
    print(years)
    print(france_data.describe)

    ### IDF 
    idf_codes = ('75','77','78','91','92','93','94','95')
    mask = france_data["Code Commune"].fillna("").astype(str).str.startswith(idf_codes)

    idf_data = france_data[mask]
    idf_data["Conso_log"] = np.log1p(idf_data["Conso totale (MWh)"])

    ### FRANCE 
    france_data["Conso_log"] = np.log1p(france_data["Conso totale (MWh)"])


    createMap(idf_data,"data/cleaned/communes_idf.geojson","commune",2023)


if __name__=="__main__":
    main()