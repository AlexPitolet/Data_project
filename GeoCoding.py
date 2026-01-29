import json
import folium


STATIONS = ['ABBEVILLE', 'AJACCIO', 'ALENCON', 'BALE-MULHOUSE',
            'BELLE ILE-LE TALUT', 'BORDEAUX-MERIGNAC', 'BOURGES',
            'BREST-GUIPAVAS', 'CAEN-CARPIQUET', 'CAP CEPET',
            'CLERMONT-FD', 'DIJON-LONGVIC', 'EMBRUN', 'GOURDON',
            'LE PUY-LOUDES', 'LILLE-LESQUIN', 'LIMOGES-BELLEGARDE',
            'LYON-ST EXUPERY', 'MARIGNANE', 'MILLAU', 'MONT-DE-MARSAN',
            'MONTELIMAR', 'MONTPELLIER', 'NANCY-OCHEY',
            'NANTES-BOUGUENAIS', 'NICE', 'ORLY', 'PERPIGNAN',
            "PLOUMANAC'H", 'POITIERS-BIARD', 'PTE DE CHASSIRON',
            'PTE DE LA HAGUE', 'REIMS-PRUNAY', 'RENNES-ST JACQUES',
            'ROUEN-BOOS', 'ST GIRONS', 'STRASBOURG-ENTZHEIM',
            'TARBES-OSSUN', 'TOULOUSE-BLAGNAC', 'TOURS', 'TROYES-BARBEREY']

LATS = [50.136, 41.918, 48.4455, 47.614333, 47.294333,
        44.830667, 47.059167, 48.444167, 49.18, 43.079333,
        45.786833, 47.267833, 44.565667, 44.745, 45.0745,
        50.57, 45.861167, 45.7265, 43.437667, 44.1185,
        43.909833, 44.581167, 43.577, 48.581, 47.15,
        43.648833, 48.716833, 42.737167, 48.825833,
        46.593833, 46.046833, 49.725167, 49.209667,
        48.068833, 49.383, 43.005333, 48.5495, 43.188,
        43.621, 47.4445, 48.324667]

LONGS = [1.834, 8.792667, 0.110167, 7.51, -3.218333, -0.691333,
         2.359833, -4.412, -0.456167, 5.940833, 3.149333, 5.088333,
         6.502333, 1.396667, 3.764, 3.0975, 1.175, 5.077833, 5.216,
         3.0195, -0.500167, 4.733, 3.963167, 5.959833, -1.608833,
         7.209, 2.384333, 2.872833, -3.473167, 0.314333, -1.4115,
         -1.939833, 4.155333, -1.734, 1.181667, 1.106833, 7.640333,
         0.0, 1.378833, 0.727333, 4.02]

TEMPS = [7.6, 13.5, 7.6, 6.8, 10.5, 11.5, 8.5, 9.7, 8.6, 11.8, 9.1,
         7.2, 5.7, 9.2, 6.0, 7.2, 7.6, 8.4, 12.0, 6.1, 11.6, 9.6, 11.7,
         6.5, 10.0, 11.7, 8.1, 12.6, 9.9, 9.1, 10.8, 9.5, 7.4, 9.0,
         7.1, 10.3, 6.7, 10.8, 10.6, 8.4, 8.1]


coords = (46.539758, 2.430331)
map1 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)

for i in range(len(STATIONS)):
    folium.CircleMarker(
        location = (LATS[i],LONGS[i]),
        radius= TEMPS[i]*2,
        color = "crimson",
        fill = True,
        fill_color= "crimson"
    ).add_to(map1)

map1.save(outfile='map1.html')


import branca
map2 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)

cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(TEMPS), vmax=max(TEMPS))
map2.add_child(cm) # add this colormap on the display

for lat, lng, size, color in zip(LATS, LONGS, TEMPS, TEMPS):
    folium.CircleMarker(
        location=[lat, lng],
        radius=size,
        color=cm(color),
        fill=True,
        fill_color=cm(color),
        fill_opacity=0.6
    ).add_to(map2)

map2.save(outfile='map2.html')


import geojson, geopandas, pandas

# lecture du fichier global
france = geopandas.read_file("datagouv-communes.geojson")

l = []
# sélection des données d'Ile de France
for dpt in ["75", "77", "78", "91", "92", "93", "94", "95"]:
    dptidf = france[france["code_commune"].str.startswith(dpt)]
    l.append(dptidf)

# construction de la GeoDataFrame correspondante
idf = pandas.concat(l)

# écriture dans un fichier
with open("idf.geojson", "w") as f:
    geojson.dump(idf, f)

coords = (48.7453229,2.5073644)
map3 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

#style function
sf = lambda x :{'fillColor':'#E88300', 'fillOpacity':0.5, 'color':'#E84000', 'weight':1, 'opacity':1}

folium.GeoJson(
    data="idf.geojson",
    name="idf",
    style_function= sf
).add_to(map3)

map3.save(outfile='map3.html')

import pandas as pd
geo_data = "idf.geojson"
pop_data = pd.read_csv('insee-pop-communes.csv', sep=';')
dpt_code = pop_data['DEPCOM']
mask = ( ( dpt_code.str.startswith('75')  )
        | ( dpt_code.str.startswith('77') )
        | ( dpt_code.str.startswith('78') )
        | ( dpt_code.str.startswith('91') )
        | ( dpt_code.str.startswith('92') )
        | ( dpt_code.str.startswith('93') )
        | ( dpt_code.str.startswith('94') )
        | ( dpt_code.str.startswith('95') ) )
pop_data = pop_data[mask]

coords = (48.7190835,2.4609723)
map4 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

folium.Choropleth(
    geo_data=geo_data,                              # geographical data
    name='choropleth',
    data=pop_data,                                  # numerical data
    columns=['DEPCOM', 'PTOT'],                     # numerical data key/value pair
    key_on='feature.properties.code_commune',       # geographical property used to establish correspondance with numerical data
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population'
).add_to(map4)

map4.save(outfile='map4.html')