import pandas as pd
from pandas import Series,DataFrame
import geopandas
import numpy as np
import shutil

df_raw=pd.read_csv("data/raw/dataset/consommation-annuelle-d-electricite-et-gaz-par-commune.csv", sep=";")  

cols1 = df_raw.loc[:,"OPERATEUR" : "Code Commune"].columns
cols2 = df_raw.loc[:,"Code Département" : "CODE GRAND SECTEUR"].columns
cols3 = df_raw.loc[:,"Conso totale (MWh)": "Conso moyenne (MWh)"].columns
cols4 = df_raw.loc[:,"Nombre d'habitants":"Superficie des logements >100 m2"].columns
cols5 = ["Taux de chauffage électrique"]

#cols = selected_cols = (
#    cols1.tolist()
#    + cols2.tolist()
#    + cols3.tolist()
#    + cols4.tolist()
#    + cols5
#)

df = df_raw.loc[:,cols1.tolist()+ cols2.tolist()+ cols3.tolist()+ cols4.tolist()+ cols5]
#print(df.info())
conso_moy_per_region ={}
annees = df["Année"].unique()
for annee in annees : 
    df_annee = df[df["Année"] == annee]
    conso_moy_per_region[annee] = {}
    for i,region in enumerate(df["Code Région"].sort_values().unique()) : 
        df_region = df_annee[df_annee["Code Région"]==region]
        if(not df_region.empty) : 
            mean_conso = df_region["Conso moyenne (MWh)"].mean()
            conso_moy_per_region[(int)(annee)][df_region["Nom Région"].mode()[0]] = (float)(mean_conso) #ajouter le mode au prétraitement ? 

print(conso_moy_per_region)

df_grouped = df.groupby(['Année', 'Nom Région'])['Conso moyenne (MWh)'].mean().reset_index()
df_grouped.to_csv("data/cleaned/conso_per_region.csv")

df_final = pd.DataFrame([
    {"Année": annee, "Nom Région": reg, "Conso moyenne (MWh)": val}
    for annee, regions in conso_moy_per_region.items()
    for reg, val in regions.items()
])
conso_moy_per_region_csv = df_final.to_csv("data/cleaned/conso_per_region2.csv")

#df_conso_moy_per_region = pd.DataFrame.from_dict(conso_moy_per_region, orient= 'index', columns=["Conso moyenne (MWh)"])
#df_conso_moy_per_region.index.name = "Nom Région"
#conso_moy_per_region_csv =df_conso_moy_per_region.to_csv("data/cleaned/conso_per_region.csv")
def clean_geojson():   
    geo_communes_dir = "data\\raw\\datagouv-communes.geojson"
    geo_dep_dir =   "data\\raw\\departements-50m.geojson"
    geo_reg_dir =   "data\\raw\\regions-50m.geojson"

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

    dep = df.groupby(["Code Département","Année"],as_index=False)["Conso totale (MWh)"].sum()
    dep.to_csv("data/cleaned/codes_et_conso_totale_departements.csv")

    reg = df.groupby(["Code Région","Année"],as_index=False)["Conso totale (MWh)"].sum()
    reg.to_csv("data/cleaned/codes_et_conso_totale_regions.csv")



def clean_all_data():
    clean_geojson()
    clean_csv()


if __name__=="__main__":
    print("Cleaning data")
    clean_all_data()
