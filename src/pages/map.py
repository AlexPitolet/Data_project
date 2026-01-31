from dash import html, dcc, Input, Output
import pandas as pd
import plotly_express as px
from src.utils.common_fuctions import select_data

level = "region"
year = 2011
consumption_type = "Conso totale (MWh)"

data, geojson, col_name, key_on, hover = select_data(level,year,consumption_type)

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
            "Conso totale (MWh)": ": .0f",  
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
                                ),
                                html.Label('Type de consommation'),
                                dcc.Dropdown(
                                    id="type-dropdown",
                                    options=[
                                        {'label': 'Consommation totale', 'value': "Conso totale (MWh)"},
                                        {'label': 'Consommation moyenne', 'value': "Conso moyenne (MWh)"},
                                    ],
                                    value="Conso totale (MWh)",
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
                                 children=[
                                    html.H3("Annalyse des données"),
                                    html.H4("Vue d’ensemble de la consommation électrique"),
                                    html.P(
                                        "Cette carte interactive représente la somme de la consommation totale d’électricité par région et par département en France entre 2011 et 2024. "
                                        "Elle met en évidence une forte hétérogénéité spatiale de la consommation sur le territoire français, avec des écarts marqués entre les zones fortement urbanisées "
                                        "et les territoires plus ruraux. Les teintes foncées traduisent une consommation élevée, tandis que les teintes claires indiquent une consommation plus modérée, "
                                        "illustrant une répartition loin d’être uniforme à l’échelle nationale."
                                    ),

                                    html.H4("Influence de la population et de l’urbanisation"),
                                    html.P(
                                        "Les régions et départements les plus consommateurs correspondent majoritairement à de grandes métropoles et agglomérations telles que l’Île-de-France, "
                                        "Lille, Lyon ou Marseille. Cette surconsommation s’explique en grande partie par la densité de population et la concentration des activités urbaines : "
                                        "services, bureaux, réseaux de transport, logements collectifs et infrastructures numériques. "
                                        "L’usage intensif de l’électricité dans le secteur tertiaire et résidentiel contribue ainsi fortement à l’intensité observée dans ces territoires."
                                    ),

                                    html.H4("Rôle de l’activité industrielle"),
                                    html.P(
                                        "La population n’est toutefois pas le seul facteur déterminant de la consommation électrique. Certaines zones apparaissent très consommatrices malgré "
                                        "une densité de population plus modérée, en raison de leur forte activité industrielle. "
                                        "Les régions industrialisées, comme les Hauts-de-France, concentrent des industries lourdes telles que la sidérurgie, la chimie ou l’agroalimentaire, "
                                        "ainsi que des plateformes logistiques et portuaires. "
                                        "À titre d’exemple, les Hauts-de-France affichent environ 100 millions de MWh de consommation totale pour près de 6 millions d’habitants, "
                                        "contre environ 140 millions de MWh pour l’Île-de-France, qui compte pourtant deux fois plus d’habitants."
                                    ),

                                    html.H4("Territoires faiblement consommateurs"),
                                    html.P(
                                        "À l’inverse, les départements les plus clairs sur la carte se situent majoritairement dans des zones rurales ou peu urbanisées, "
                                        "caractérisées par une faible densité de population et une activité économique limitée. "
                                        "Dans ces territoires, la consommation électrique est réduite en raison d’un nombre moindre de logements, "
                                        "d’un tissu industriel peu développé et de modes de chauffage parfois alternatifs à l’électricité, "
                                        "comme le bois, le fioul ou le gaz."
                                    ),

                                    html.H4("Apport de l’échelle départementale"),
                                    html.P(
                                        "Le passage à une échelle départementale permet de mettre en évidence des nuances importantes au sein même des régions. "
                                        "Une région globalement moyenne peut masquer de forts contrastes internes, avec un département très consommateur entouré "
                                        "de départements nettement plus sobres. "
                                        "Cette lecture à échelle fine souligne que la consommation électrique n’est pas homogène au sein d’un même territoire régional "
                                        "et qu’une analyse détaillée est essentielle pour comprendre les dynamiques locales."
                                    ),

                                    html.H4("Lecture globale et facteurs explicatifs"),
                                    html.P(
                                        "La consommation d’électricité d’un territoire dépend ainsi d’une combinaison de facteurs socio-économiques : "
                                        "densité et répartition de la population, degré d’urbanisation, poids de l’activité industrielle et tertiaire, "
                                        "usages domestiques de l’énergie ainsi que présence d’infrastructures de transport et de services. "
                                        "La carte illustre donc une logique multifactorielle, mettant en lumière des disparités structurelles "
                                        "plutôt qu’un simple effet géographique."
                                    ),




                                            
                        ],
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
        [Input(component_id='year-dropdown', component_property='value'),
         Input(component_id='scale-dropdown', component_property='value'),
         Input(component_id="type-dropdown", component_property="value")
         ]
    )
    def update_figure(year, scale,cons_type): 
        data, geojson, col_name, key_on, hover = select_data(scale,year,cons_type)
        fig = px.choropleth_map(
            data_frame=data,
            geojson=geojson,
            featureidkey=key_on,
            locations=col_name,
            color=cons_type,
            color_continuous_scale="YlGn",  
            hover_name= hover,
            hover_data={
                col_name: True,             
                cons_type: ": .0f",  
            },
            center={"lat": 46.6, "lon": 2.5},  # centre de la France
            zoom=5,
            ) # (4)
        title = f"Carte de la consommation d'électricité totale entre {year} au niveau {scale}"
        
        return fig,title