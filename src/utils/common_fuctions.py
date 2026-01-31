from typing import Literal
import json
import os
import pandas as pd 

def select_data(level:Literal["commune","departement","region"],year):
    data_dir = "data/cleaned"

    if level == "commune":
        col_name = 'Code Commune'
        geojson_path = os.path.join(data_dir,"communes_france.geojson")
        with open(geojson_path) as f:
            geojson = json.load(f)
        key_on = 'properties.code_commune'

    elif level == "departement":
        data = pd.read_csv(os.path.join(data_dir,"codes_et_conso_totale_departements.csv"))
        data = data.query(f"Année=={year}")
        col_name = 'Code Département'

        data[col_name] = data[col_name].astype(str).str.zfill(2) # Evitement de l'incompatibilité entre les codes dep du csv et du geojson

        geojson_path = os.path.join(data_dir,"departements.geojson")
        with open(geojson_path) as f:
            geojson = json.load(f)
        data = data.groupby(col_name,as_index=False)["Conso totale (MWh)"].sum()
        key_on = 'properties.code'

    elif level == "region":
        data = pd.read_csv(os.path.join(data_dir,"codes_et_conso_totale_regions.csv"))
        data = data.query(f"Année=={year}")
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