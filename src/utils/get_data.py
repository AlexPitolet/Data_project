import urllib.request
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

#RAW_DATA_DIR = "/data/raw"
#RAW_DATA_DIR = "data/raw"
NB_DATA = 4 # à modifier en fonction du nb de fichier à obtenir au final dans data/raw 

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

    urllib.request.urlretrieve(url, os.path.join(RAW_DATA_DIR,file_name))
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

def checkData():
    if(not os.path.exists(RAW_DATA_DIR)):
        print(f"Dir {RAW_DATA_DIR} doesn't exist...\nCreation of the directory")
        os.mkdir(RAW_DATA_DIR)
    return len(os.listdir(RAW_DATA_DIR)) == NB_DATA

def get_all_data():
    print("Checking if dataset is installed")
    if(not checkData()):
        print("Dataset not installed !\nStarting download...")
        get_data()
        print("Dataset successfully downloaded")    
    else : 
        print("Data already downloaded")  

    