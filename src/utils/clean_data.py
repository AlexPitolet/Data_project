import pandas as pd
from pandas import Series,DataFrame
import geopandas
import numpy as np

data = pd.read_csv("data/raw/consommation-annuelle-d-electricite-et-gaz-par-commune.csv")



def clean_geojson():   
    geo_data_dir = "data\\raw\\datagouv-communes.geojson"
    

    # lecture du fichier global
    france = geopandas.read_file(geo_data_dir)
    france.to_file("data\\cleaned\\communes_france.geojson")

    l = []
    # sélection des données d'Ile de France
    for dpt in ["75", "77", "78", "91", "92", "93", "94", "95"]:
        dptidf = france[france["code_commune"].str.startswith(dpt)]
        l.append(dptidf)

    # construction de la GeoDataFrame correspondante
    idf = pd.concat(l)

    # écriture dans un fichier
    idf.to_file("data\\cleaned\\communes_idf.geojson", driver="GeoJSON")



if __name__=="__main__":
    clean_geojson()