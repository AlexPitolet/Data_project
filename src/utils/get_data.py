import urllib.request
import os

RAW_DATA_DIR = "data/raw"

def get_geojson():
    ### Get France cities borders geojson
    url = "https://perso.esiee.fr/~courivad/courses/EPIGEP-FI-3-S1-UPM-Python-visualisation-donnees/_downloads/52338df481935edd0f0adb1ac3154f5f/datagouv-communes.geojson"
    file_name = "datagouv-communes.geojson"

    urllib.request.urlretrieve(url, os.path.join(RAW_DATA_DIR,file_name))

    ### Get France departements borders geojson
    url = "https://adresse.data.gouv.fr/data/contours-administratifs/2023/geojson/departements-50m.geojson"
    file_name = "departements-50m.geojson"

    urllib.request.urlretrieve(url, os.path.join(RAW_DATA_DIR,file_name))

    ### Get France regions borders geojson
    url = "https://adresse.data.gouv.fr/data/contours-administratifs/2023/geojson/regions-50m.geojson"
    file_name = "regions-50m.geojson"

    urllib.request.urlretrieve(url, os.path.join(RAW_DATA_DIR,file_name))

    return

def get_csv():
    url = "https://www.data.gouv.fr/api/1/datasets/r/b73dda82-ba8e-44f5-ac41-1c14959c67f7"
    file_name = "consommation-annuelle-d-electricite-et-gaz-par-commune.csv"

    urllib.request.urlretrieve(url, os.path.join("",file_name))
    return


def get_data():  
    print(f"Data path : {RAW_DATA_DIR}")
    print("Downloading CSV data")
    get_csv()
    print("CSV successfully downloaded")

    print("Downloading GEOJSON data")
    get_geojson()
    print("GEOJSONs files successfully downloaded")
    return


if __name__=="__main__":
    get_data()