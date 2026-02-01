import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output
import numpy as np

df = pd.read_csv("data/cleaned/conso_per_region.csv")
annees_disponibles = sorted(df["Année"].unique())

layout = html.Div(children=[

                        html.H1(children='Histogramme dynamique représentant la consommation moyenne d\'énergie par région ',
                                    style={'textAlign': 'center', 'color': '#7FDBFF'}), 

                        html.Div([
                            # Colonne de GAUCHE : Contrôles
                            html.Div([
                                html.Div([
                                    html.Label("Année d'analyse", style={'fontWeight': 'bold'}),
                                    dcc.Slider(
                                        id='year-slider',
                                        min=min(annees_disponibles),
                                        max=max(annees_disponibles),
                                        value=max(annees_disponibles), # Valeur par défaut
                                        marks={str(year): str(year) for year in annees_disponibles},
                                        step=None
                                    ),
                                ], style={'marginBottom': '30px'}),
                                html.Div([
                                    html.Label("Métrique", style={'fontWeight': 'bold'}),
                                    dcc.Dropdown(
                                        id="metric-dropdown",
                                        options=[
                                            {"label": "Moyenne nationale", "value": "mean"},
                                            {"label": "Consommation minimale", "value": "min"},
                                            {"label": "Consommation maximale", "value": "max"}
                                        ],
                                        value="mean",
                                        clearable=False,
                                    ),
                                ]),
                                # Affichage de ma métrique juste en dessous des filtres
                                html.Div(id="reference-value", style={
                                    'marginTop': '40px',
                                    'padding': '20px',
                                    'backgroundColor': "#cccdce",
                                    'borderRadius': '10px',
                                    'textAlign': 'center'
                                }),
                            ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
                        
                            # Colonne de DROITE : Graphique
                            html.Div([
                                dcc.Graph(id='graphConso', style={'height': '70vh'}),
                                html.P("Description du graphique : Ce bar chart compare la consommation lissée par point de livraison.",
                                style={'fontSize': '12px', 'color': 'gray', 'marginTop': '10px'})
                            ], style={'width': '70%', 'display': 'inline-block', 'padding': '20px'})
                        ], style={'display': 'flex', 'flexDirection': 'row'}),

                        html.Div(id="desc",
                                 children=[
                                    html.H3("Analyse des données"),

                                    html.H4("Description du graphique"),
                                    html.P(
                                        "Ce graphique représente la consommation électrique moyenne 'lissée'. Contrairement à la consommation totale, "
                                        "cet indicateur divise l'énergie consommée par le nombre de points de livraison dans la région (compteurs). " 
                                        "Cela permet de comparer des régions de tailles différentes (ex: Île-de-France vs Bretagne) sur une base de 'consommation par site'."
                                        "Chaque région possède sa couleur et la taille d'une barre dans l'histogramme est proportionnelle"
                                        "à la consommation de la région associée. N'hésitez pas à passer la souris par dessus le graphique pour plus de détails."
                                        " L'animation (disponible via le bouton play) permet de visualiser l'évolution de cette consommation moyenne par région au fil des années."
                                    ),
                                    
                                    html.H4("Changement méthodologique important en 2018"),
                                    html.P(
                                        "Un changement significatif dans la collecte des données s'est opéré en 2018. La méthodologie de comptage des sites de livraison "
                                        "a été réformée, affectant le calcul de la consommation moyenne par région. "
                                        "La base de division ayant augmenté, la moyenne par site a mécaniquement chuté."
                                        "On estime cette baisse à environ 50" "%" ", concernant toutes les régions après le passage de 2017 à 2018. "
                                        "Cependant, cette baisse est principalement un artefact statistique dû au changement de méthodologie de comptage, et non une diminution réelle de la consommation d'énergie. "
                                        "Les utilisateurs doivent être conscients de ce changement méthodologique lors de la comparaison des données antérieures à 2018 avec 2018 et après. "
                                        "Les tendances observées avant et après 2018 ne doivent pas être directement comparées sans tenir compte de cette rupture structurelle."
                                    ),

                                    html.H4("Zoom sur les Territoires d'Outre-Mer"),
                                    html.P(
                                        "Les données pour certaines régions comme la Corse ou la Guyane peuvent afficher des valeurs nulles ou "
                                        "très faibles sur certaines périodes. Cela traduit souvent une remontée de données incomplète dans les fichiers "
                                        "sources open-data pour ces zones géographiques spécifiques avant leur intégration complète."
                                        "Par convention, ces valeurs nulles sont prises en compte dans le calcul des métriques"
                                        "Par conséquent, plusieurs années peuvent afficher une consommation minimum de 0 MWh à cause de ces régions."
                                    ),

                                    html.H4("Facteurs de variabilité"),
                                    html.P(
                                        "On peut en conclure ces moyennes sont influencées par plusieurs facteurs : climat, densité de population, activités et secteurs économiques dominants."
                                        "En guise d'exemple, les différences entre régions peuvent s'expliquent par le profil économique : les régions à forte densité industrielle "
                                        "(Hauts-de-France, Normandie) présentent souvent des moyennes par site plus élevées que les régions "
                                        "principalement résidentielles ou touristiques. De plus, certaines régions chaudes les DOM-TOM ont des consommations moyennes plus basses en raison d'un moindre besoin de chauffage. "
                                        "Cela dit, pour mettre en lumière la pluralité des facteurs à prendre en compte, on observe que la Provence-Alpes-Côte d'Azur,"
                                        "théoriquement plus chaude, affiche des consommations moyennes particulièrement élevées, probablement en raison de son urbanisation et de son tourisme intensif."
                                    ),
                                            
                        ],
                        style={
                            "margin":"auto",
                            "width":"50vw",
                            "textAlign": "justify"
                        })

]
)

def register_callback(app):
# --- CALLBACK ---
    @app.callback(
        Output('graphConso', 'figure'),
        Input("metric-dropdown", "value"),
        Input('year-slider', 'value')
    )
    def update_figure(_,__): #aucun des inputs n'est utilisé pour le moment, mais plotly n'accepte pas les callbacks sans input
        temp_df = df.copy() #évite les warnings, impact minime sur la performance
        temp_df["Conso moyenne (MWh)"] = temp_df["Conso moyenne (MWh)"].replace([np.inf, -np.inf], 0).fillna(0)
        fig = px.bar(
            temp_df,
            x="Nom Région",
            y="Conso moyenne (MWh)",
            color="Nom Région",
            animation_frame="Année", #permet de faire une animation par année
            title="Consommation d'énergie moyenne par région",
            range_y=[0, temp_df["Conso moyenne (MWh)"].max() * 1.1] #permet d'avoir une échelle fixe pour l'axe y
        )

        # Cosmétique
        fig.update_layout(
            transition_duration=800,
            xaxis_title="Région",
            yaxis_title="Consommation moyenne (MWh)",
            xaxis_tickangle=-45,
            showlegend=False,
        )

        fig.update_traces(
            hovertemplate=
            "Région : %{x}<br>" +
            "Conso moyenne : %{y:.0f} MWh<extra></extra>" # <extra></extra> supprime la trace générée automatiquement par plotly, mais ajoute le hover "Année"
        )
        return fig

    @app.callback(
        Output("reference-value", "children"),
        Input("metric-dropdown", "value"),
        Input('year-slider', 'value')
    )
    def update_reference(selected_metric, selected_year):
        #calcul de la métrique sélectionnée en fonction de l'année sélectionnée
        filtered_df = df[df["Année"] == selected_year].copy()
        filtered_df["Conso moyenne (MWh)"] = filtered_df["Conso moyenne (MWh)"].replace([np.inf, -np.inf], np.nan).fillna(0)
        if selected_metric == "mean":
            val = filtered_df["Conso moyenne (MWh)"].mean()
            label = "Moyenne nationale"
        elif selected_metric == "min":
            val = filtered_df["Conso moyenne (MWh)"].min()
            label = "Consommation minimale"
        else:
            val = filtered_df["Conso moyenne (MWh)"].max()
            label = "Consommation maximale"

        return f"{label} : {val:.0f} MWh"

# --- END CALLBACK ---