from typing import Literal
import json
import os
import pandas as pd 

DATA_DIR = "data/cleaned"

def select_csv(level:Literal["departement","region"], consumption_type:Literal["Conso totale (MWh)","Conso moyenne (MWh)"]):
    if(consumption_type == "Conso totale (MWh)"):
        if(level == "departement"):
            csv_filename = "conso_totale_departements.csv"
        elif(level == "region"):
            csv_filename = "conso_totale_regions.csv"
        else: 
            print(f"Erreur de level : {level}\n")
            return

    elif (consumption_type == "Conso moyenne (MWh)"):
        if(level == "departement"):
            csv_filename = "conso_moy_departements.csv"
        elif(level == "region"):
            csv_filename = "conso_moy_regions.csv"
        else: 
            print(f"Erreur de level : {level}\n")
            return
    else: 
        print(f"Erreur de type de consommation : {consumption_type};\nType de consommation automatiquement mis à \"Conso totale (MWh)\"")
        consumption_type = "Conso totale (MWh)"

    return pd.read_csv(os.path.join(DATA_DIR,csv_filename))



def select_data(level:Literal["departement","region"],year:int,consumption_type:Literal["Conso totale (MWh)","Conso moyenne (MWh)"]):
    """Sélectionne les bonnes données en fonction de l'échelle et de l'année"""
    
    if year == None:
        print(f"Erreur d'année : {year};\nAnnée automatiquement mis à 2011")
        year = 2011

    if level == "departement":
        data = select_csv(level, consumption_type)
        data = data.query(f"Année=={year}")
        col_name = 'Code Département'
        hover = 'Nom Département'
        data[col_name] = data[col_name].astype(str).str.zfill(2) # Evitement de l'incompatibilité entre les codes dep du csv et du geojson
        data = data.groupby([col_name,hover],as_index=False)[consumption_type].sum()

        geojson_path = os.path.join(DATA_DIR,"departements.geojson")
        with open(geojson_path) as f:
            geojson = json.load(f)
        
        key_on = 'properties.code'

    elif level == "region":
        data = select_csv(level, consumption_type)
        data = data.query(f"Année=={year}")
        col_name = 'Code Région'
        hover = 'Nom Région'
        data[col_name] = data[col_name].astype(str).str.zfill(2) # Evitement de l'incompatibilité entre les codes dep du csv et du geojson
        data = data.groupby([col_name,hover],as_index=False)[consumption_type].sum()
        
        geojson_path = os.path.join(DATA_DIR,"regions.geojson")
        with open(geojson_path) as f:
            geojson = json.load(f)
        
        key_on = 'properties.code'

    else:
        print(f"Erreur de level : {level}")
        return

    return data, geojson, col_name, key_on, hover