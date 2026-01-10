import pandas as pd
from pandas import Series,DataFrame

data = pd.read_csv("data/raw/consommation-annuelle-d-electricite-et-gaz-par-commune.csv")

df = DataFrame()


for col in data:
    if not(col.unique() is None):
        pd.concat([df, Series.to_frame(), axis=1])