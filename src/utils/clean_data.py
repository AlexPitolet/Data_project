import pandas as pd
import numpy as np

df_raw=pd.read_csv("data/raw/dataset/consommation-annuelle-d-electricite-et-gaz-par-commune.csv", sep=";")  

cols1 = df_raw.loc[:,"OPERATEUR" : "Nom Commune"].columns
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
df.to_csv("data/cleaned/cleanedDataset.csv")