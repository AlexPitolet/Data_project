from dash import html, dcc, Input, Output
import pandas as pd
import plotly_express as px
from src.utils.common_fuctions import select_data

level = "region"
year = 2011

data, geojson, col_name, key_on, hover = select_data(level,year)

fig = px.choropleth_map(
        data_frame=data,
        geojson=geojson,
        featureidkey=key_on,
        locations=col_name,
        color="Conso totale (MWh)",
        color_continuous_scale="YlGn",
        hover_name= hover,
        hover_data={
            col_name: True,             
            "Conso totale (MWh)": ":,.0f",  
        },
        center={"lat": 46.6, "lon": 2.5},  # centre de la France
        zoom=5,
        )

layout = html.Div([ 
                        html.H1(id='H1',
                            children=f"Carte de la consommation d'électricité totale entre {year}",        
                            style={
                                'textAlign': 'center', 
                                'color': '#7FDBFF',
                            }
                        ),
                        html.Div([
                            html.Div([
                                html.Label('Année'),
                                dcc.Dropdown(
                                    id="year-dropdown",
                                    options=[
                                        {'label': '2011', 'value': 2011},
                                        {'label': '2012', 'value': 2012},
                                        {'label': '2013', 'value': 2013},
                                        {'label': '2014', 'value': 2014},
                                        {'label': '2015', 'value': 2015},
                                        {'label': '2016', 'value': 2016},
                                        {'label': '2017', 'value': 2017},
                                        {'label': '2018', 'value': 2018},
                                        {'label': '2019', 'value': 2019},
                                        {'label': '2020', 'value': 2020},
                                        {'label': '2021', 'value': 2021},
                                        {'label': '2022', 'value': 2022},
                                        {'label': '2023', 'value': 2023},
                                        {'label': '2024', 'value': 2024},
                                    ],
                                    value=2011,
                                ),
                                html.Label('Échelle'),
                                dcc.Dropdown(
                                    id="scale-dropdown",
                                    options=[
                                        #{'label': 'Commune', 'value': "commune"},
                                        {'label': 'Département', 'value': "departement"},
                                        {'label': 'Région', 'value': "region"},
                                    ],
                                    value="region",
                                )
                                ],
                                style={
                                    "display":"flex",
                                    "flexDirection":"column",
                                    "width":"20vw",
                                }),
                                dcc.Graph(
                                    id='map',
                                    #figure=fig,
                                    style={"height": "80vh","width":"60vw"}
                                )
                            ],
                            style={
                                "display":"flex",
                                "alignItems":"center",
                                "justifyContent":"center",
                                "witdh":"100%"
                            }
                            ),
                        
                        html.Div(id="desc",
                                 children=f'''
                            Cette carte intéractive représente la somme de la consommation totale de chaque régions et département de France entre 2011 et 2024.
                            \n
                            La carte met en évidence une forte disparité géographique de la consommation d’électricité sur le territoire français.
                            Certaines zones apparaissent nettement plus consommatrices (teintes foncées)
                            D’autres, plus rurales ou moins peuplées, présentent une consommation nettement plus faible (teintes claires)
                            Cette hétérogénéité reflète avant tout des différences de population, d’activités économiques et d’usages énergétiques.
                            \n\n
                            Les régions et départements les plus foncés correspondent majoritairement à :
                            Grandes métropoles
                            Exemples visibles sur la carte :
                            Île-de-France
                            Grandes agglomérations du Nord et du Sud-Est (Lille, Lyon, Marseille)
                            \n
                            Pourquoi?
                            Forte densité de population
                            Concentration de bureaux, transports, services
                            Usage massif de l’électricité (tertiaire, logements collectifs, data centers…)

                            Territoires industrialisés
                            Certaines zones très foncées peuvent aussi s’expliquer par :
                            Présence d’industries lourdes (sidérurgie, chimie, agroalimentaire)
                            Activités portuaires ou logistiques
                            Zones économiques spécifiques
                            Même avec une population modérée, l’industrie peut entraîner une consommation électrique élevée.
                            \n\n
                            Les départements les plus clairs se situent principalement :
                            Dans des zones rurales
                            Avec une faible densité de population
                            Peu industrialisées
                            \n
                            Explications possibles :
                            Moins d’habitants → moins de logements à alimenter
                            Activité économique limitée
                            Habitat individuel parfois chauffé autrement que par l’électricité (bois, fioul, gaz)
                            \n\n
                            Le passage à l’échelle départementale permet d’observer des nuances importantes :
                            Une région globalement moyenne peut cacher :
                            un département très consommateur
                            entouré de départements beaucoup plus sobres
                            \n
                            Cela montre que :
                            la consommation n’est pas homogène à l’intérieur d’une région
                            l’échelle fine est essentielle pour comprendre les dynamiques locales

                            La consommation électrique d’un territoire dépend principalement de :
                            Population et densité
                            Activité industrielle
                            Urbanisation
                            Présence du secteur tertiaire
                            Usages domestiques (chauffage, climatisation)
                            Infrastructures de transport
                            La carte illustre donc une combinaison de facteurs socio-économiques, plus qu’un simple effet géographique.

                            La consommation d’électricité en France n’est pas uniformément répartie.
                            Elle est fortement corrélée à l’urbanisation, à l’activité économique et à la densité de population, ce qui explique les écarts marqués observés entre les territoires.
                        ''',
                        style={
                            "margin":"auto",
                            "width":"50vw",
                            "textAlign": "justify"
                        })
        ])
    
def register_callback(app):
    @app.callback(
        Output(component_id='map', component_property='figure'), 
        Output(component_id='H1', component_property='children'),
        Output(component_id="desc",component_property='children'),
        [Input(component_id='year-dropdown', component_property='value'),
         Input(component_id='scale-dropdown', component_property='value')] # (2)
    )
    def update_figure(year, scale): # (3)
        data, geojson, col_name, key_on, hover = select_data(scale,year)
        fig = px.choropleth_map(
            data_frame=data,
            geojson=geojson,
            featureidkey=key_on,
            locations=col_name,
            color="Conso totale (MWh)",
            color_continuous_scale="YlGn",  
            hover_name= hover,
            hover_data={
                col_name: True,             
                "Conso totale (MWh)": ":,.0f",  
            },
            center={"lat": 46.6, "lon": 2.5},  # centre de la France
            zoom=5,
            ) # (4)
        title = f"Carte de la consommation d'électricité totale entre {year} au niveau {scale}"
        desc = f'''
                            Cette carte intéractive représente la somme de la consommation totale de chaque régions et département de France entre 2011 et 2024.
                            \n
                            La carte met en évidence une forte disparité géographique de la consommation d’électricité sur le territoire français.
                            Certaines zones apparaissent nettement plus consommatrices (teintes foncées)
                            D’autres, plus rurales ou moins peuplées, présentent une consommation nettement plus faible (teintes claires)
                            Cette hétérogénéité reflète avant tout des différences de population, d’activités économiques et d’usages énergétiques.
                            \n\n
                            Les régions et départements les plus foncés correspondent majoritairement à :
                            Grandes métropoles
                            Exemples visibles sur la carte :
                            Île-de-France
                            Grandes agglomérations du Nord et du Sud-Est (Lille, Lyon, Marseille)
                            \n
                            Pourquoi?
                            Forte densité de population
                            Concentration de bureaux, transports, services
                            Usage massif de l’électricité (tertiaire, logements collectifs, data centers…)

                            Territoires industrialisés
                            Certaines zones très foncées peuvent aussi s’expliquer par :
                            Présence d’industries lourdes (sidérurgie, chimie, agroalimentaire)
                            Activités portuaires ou logistiques
                            Zones économiques spécifiques
                            Même avec une population modérée, l’industrie peut entraîner une consommation électrique élevée.
                            \n\n
                            Les départements les plus clairs se situent principalement :
                            Dans des zones rurales
                            Avec une faible densité de population
                            Peu industrialisées
                            \n
                            Explications possibles :
                            Moins d’habitants → moins de logements à alimenter
                            Activité économique limitée
                            Habitat individuel parfois chauffé autrement que par l’électricité (bois, fioul, gaz)
                            \n\n
                            Le passage à l’échelle départementale permet d’observer des nuances importantes :
                            Une région globalement moyenne peut cacher :
                            un département très consommateur
                            entouré de départements beaucoup plus sobres
                            \n
                            Cela montre que :
                            la consommation n’est pas homogène à l’intérieur d’une région
                            l’échelle fine est essentielle pour comprendre les dynamiques locales

                            La consommation électrique d’un territoire dépend principalement de :
                            Population et densité
                            Activité industrielle
                            Urbanisation
                            Présence du secteur tertiaire
                            Usages domestiques (chauffage, climatisation)
                            Infrastructures de transport
                            La carte illustre donc une combinaison de facteurs socio-économiques, plus qu’un simple effet géographique.

                            La consommation d’électricité en France n’est pas uniformément répartie.
                            Elle est fortement corrélée à l’urbanisation, à l’activité économique et à la densité de population, ce qui explique les écarts marqués observés entre les territoires.
                '''
        return fig,title,desc