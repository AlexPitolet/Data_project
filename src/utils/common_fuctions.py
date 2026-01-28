from typing import Literal
import json
import os

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