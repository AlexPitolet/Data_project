import pandas as pd
from pandas import Series,DataFrame
import geopandas
import numpy as np
import shutil

data = pd.read_csv("data/raw/consommation-annuelle-d-electricite-et-gaz-par-commune.csv")

def clean_geojson():   
    geo_communes_dir = "data\\raw\\datagouv-communes.geojson"
    geo_dep_dir =   "data\\raw\\departements-50m.geojson"
    geo_reg_dir =   "data\\raw\\datagouv-communes.geojson"

    ### Communes
    # lecture du fichier global
    france = geopandas.read_file(geo_communes_dir)
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

    ### Departements
    dest = "data/cleaned/departements.geojson"
    shutil.copyfile(geo_dep_dir,dest)

    ### Regions
    dest = "data/cleaned/regions.geojson"
    shutil.copyfile(geo_reg_dir,dest)


def clean_csv():
    data = pd.read_csv("data/raw/consommation-annuelle-d-electricite-et-gaz-par-commune.csv")
    df = data[["Année","Code Région","Code Département","Code Commune","Conso totale (MWh)"]]
    df.to_csv("data/cleaned/codes_et_conso_totale.csv")

def clean_all_data():
    clean_geojson()
    clean_csv()


if __name__=="__main__":
    print("Cleaning data")
    clean_all_data()