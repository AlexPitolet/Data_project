import pandas as pd
import numpy as np
import shutil
import os

CLEAN_DATA_DIR = "data/cleaned"
NB_DATA = 8 # Number of files in CLEAN_DATA_DIR AFTER the cleaning


def clean_geojson():   
    geo_dep_dir =   "data/raw/departements-50m.geojson"
    geo_reg_dir =   "data/raw/regions-50m.geojson"

    ### Departements
    dest = "data/cleaned/departements.geojson"
    shutil.copyfile(geo_dep_dir,dest)       #3

    ### Regions
    dest = "data/cleaned/regions.geojson"
    shutil.copyfile(geo_reg_dir,dest)       #4


def clean_csv():
    data = pd.read_csv("data/raw/consommation-annuelle-d-electricite-et-gaz-par-commune.csv", low_memory=False)
    df = data[["Année","Code Région","Nom Région","Code Département","Nom Département","Code Commune","Conso totale (MWh)","Conso moyenne (MWh)"]]
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.to_csv("data/cleaned/conso_totale.csv")     #5

    dep = df.groupby(["Code Département","Année","Nom Département"],as_index=False)["Conso totale (MWh)"].sum()
    dep.to_csv("data/cleaned/conso_totale_departements.csv")   #6

    reg = df.groupby(["Code Région","Année","Nom Région"],as_index=False)["Conso totale (MWh)"].sum()
    reg.to_csv("data/cleaned/conso_totale_regions.csv")    #7
    
    dep = df.groupby(["Code Département","Année","Nom Département"],as_index=False)["Conso moyenne (MWh)"].mean().reset_index()
    dep.to_csv("data/cleaned/conso_moy_departements.csv")   #8

    reg = df.groupby(["Code Région","Année","Nom Région"],as_index=False)["Conso moyenne (MWh)"].mean().reset_index()
    reg.to_csv("data/cleaned/conso_moy_regions.csv")    #9
    
    cols1 = data.loc[:,"OPERATEUR" : "Code Commune"].columns
    cols2 = data.loc[:,"Code Département" : "CODE GRAND SECTEUR"].columns
    cols3 = data.loc[:,"Conso totale (MWh)": "Conso moyenne (MWh)"].columns
    cols4 = data.loc[:,"Nombre d'habitants":"Superficie des logements >100 m2"].columns
    cols5 = ["Taux de chauffage électrique"]

    df = data.loc[:,cols1.tolist()+ cols2.tolist()+ cols3.tolist()+ cols4.tolist()+ cols5]
    df = df.replace([np.inf, -np.inf], np.nan)
    
    region_mapping = df[["Code Région", "Nom Région"]].drop_duplicates().set_index("Code Région")["Nom Région"].to_dict() #mapping code région -> nom région
    
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
            else : 
                conso_moy_per_region[(int)(annee)][region_mapping[region]] = 0.0


    df_final = pd.DataFrame([
        {"Année": annee, "Nom Région": reg, "Conso moyenne (MWh)": val}
        for annee, regions in conso_moy_per_region.items()
        for reg, val in regions.items()
    ])
    df_final = df_final.sort_values(by=["Année", "Nom Région"]).reset_index(drop=True)
    df_final["Conso moyenne (MWh)"] = df_final["Conso moyenne (MWh)"].replace([np.inf, -np.inf], np.nan).fillna(0)
    df_final.to_csv("data/cleaned/conso_per_region.csv")


def clean_data():
    clean_geojson()
    clean_csv()

def checkData():
    if(not os.path.exists(CLEAN_DATA_DIR)):
        print(f"Dir {CLEAN_DATA_DIR} doesn't exist...\nCreation of the directory")
        os.mkdir(CLEAN_DATA_DIR)
    return len(os.listdir(CLEAN_DATA_DIR)) == NB_DATA

def clean_all_data():
    print("Checking if data has been cleaned")
    if(not checkData()):
        print("Cleaning data")
        clean_data()
        print("Data successfully cleaned")    
    else: 
        print("Data already cleaned")  
