import pandas as pd
import numpy as np

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
print(df.info())

conso_moy_per_region ={}
for i,region in enumerate(df["Code Région"].sort_values().unique()) : 
    df_region = df[df["Code Région"]==region]
    mean_conso = df_region["Conso moyenne (MWh)"].mean()
    conso_moy_per_region[df_region["Nom Région"].mode()[0]] = (float)(mean_conso) #ajouter le mode au prétraitement ? 

print(conso_moy_per_region)

df_conso_moy_per_region = pd.DataFrame.from_dict(conso_moy_per_region, orient= 'index', columns=["Conso moyenne (MWh)"])
df_conso_moy_per_region.index.name = "Nom Région"
conso_moy_per_region_csv =df_conso_moy_per_region.to_csv("data/cleaned/conso_per_region.csv")