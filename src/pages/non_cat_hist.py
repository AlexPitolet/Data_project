import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output


df = pd.read_csv("data/cleaned/conso_totale.csv", low_memory=False) # pour les warnings
annees_disponibles = sorted(df["Année"].unique())
df_hist = df[["Code Commune", "Conso totale (MWh)", "Année"]]


layout = html.Div(children=[

                        html.H1(children=f"Distribution de la consommation totale d'énergie des communes",
                                    style={'textAlign': 'center', 'color': '#7FDBFF'}), 

                        #Year Slider
                        html.Div([
                            html.Label("Sélectionnez l'année :"),
                            dcc.Slider(
                                id='year-slider-hist',
                                min=min(annees_disponibles),
                                max=max(annees_disponibles),
                                value=min(annees_disponibles), # Valeur par défaut
                                marks={str(year): str(year) for year in annees_disponibles},
                                step=None # Permet de ne cliquer que sur les années existantes
                            ),
                        ], style={'padding': '20px'}),

                        dcc.Graph(
                            id='non_cat_hist',
                        ), 
                        
                        html.Div(
                                id="desc-hist",
                                children=[
                                    html.H3("Analyse de la distribution"),

                                    html.H4("Description du graphique"),
                                    html.P(
                                        "Ce graphe montre la distribution de la consommation totale d’électricité (en MWh) des communes françaises."
                                        "Chaque barre de l’histogramme représente un intervalle de valeurs de consommation, et sa hauteur correspond "
                                        "au nombre de communes dont la consommation se situe dans cet intervalle."
                                        "L’axe horizontal indique les classes de consommation, tandis que l’axe vertical traduit la fréquence des communes associées à chaque classe."
                                        "Ce type de représentation permet d’analyser la répartition globale des consommations, de mettre en évidence"
                                        "une éventuelle asymétrie, ainsi que la présence de communes fortement consommatrices par rapport à la majorité."
                                        "Passez la souris sur les barres pour obtenir des informations détaillées sur chaque intervalle."
                                    ),

                                    html.H4("Interprétation de l'échelle logarithmique"),
                                    html.P(
                                        "Ce graphique utilise une échelle logarithmique (log10) sur l'axe horizontal. "
                                        "Cette méthode est indispensable pour visualiser simultanément des communes rurales consommant "
                                        "quelques MWh et des métropoles dépassant le TWh. "
                                    ),

                                    html.H4("Hétérogénéité et disparités"),
                                    html.P(
                                        "La distribution révèle souvent une forme de 'courbe en cloche' décalée, indiquant que la majorité "
                                        "des communes françaises se situent dans une tranche de consommation médiane. Cependant, "
                                        "la présence de communes à 'très faible consommation' (indiquées en haut à droite du graphique) "
                                        "met en lumière l'écart abyssal entre les plus petits villages et les grandes métropoles. Ces communes, consommant moins de 1 MWh par an, "
                                        "correspondent à des zones très peu peuplées  où les "
                                        "points de livraison électrique sont quasi inexistants. On trouve également des communes dont"
                                        "la consommation est aberrament élevée, souvent liées à des activités industrielles lourdes ou à de grandes agglomérations."
                                    ),

                                    html.H4("Utilité de l'analyse temporelle"),
                                    html.P(
                                        "En déplaçant le curseur des années, on peut observer le glissement de la distribution. "
                                        "Un déplacement de la répartition vers la gauche pourrait traduire une amélioration globale "
                                        "de l'efficacité énergétique ou une baisse d'activité, cependant, nous pouvons voir que la forme "
                                        "de la courbe reste relativement stable au fil des années, on peut en déduire que peu de communes"
                                        "ont connu des changements drastiques dans leur consommation totale d'énergie sur la période étudiée."
                                    ),
                                ],
                                style={
                                    "margin": "40px auto",
                                    "width": "60vw",
                                    "textAlign": "justify",
                                    "lineHeight": "1.6"
                                })
    

]
)

def register_callback(app):
# --- CALLBACK ---
    @app.callback(
        Output('non_cat_hist', 'figure'),
        Input('year-slider-hist', 'value')
    )
    def update_figure(selected_year):
        df_year = df_hist[df_hist["Année"] == selected_year]  # d'abord filtrer par année
        # une ligne n'est pas une commune, il peut y avoir plusieurs lignes par commune (car plusieurs secteurs pour un même commune), donc on agrège et somme par commune
        df_year = df_year.groupby("Code Commune", as_index=False).agg({"Conso totale (MWh)": "sum"}) 

        df_year = df_year[df_year["Conso totale (MWh)"] > 0] #on enlève les consommations nulles ou négatives pour le log
        df_tres_faible = df_year[df_year["Conso totale (MWh)"] <= 1] #communes à très faible consommation
        
        nb_tres_faible = df_tres_faible["Code Commune"].nunique() #nombre de communes à très faible consommation, utile pour l'annotation

        df_log = df_year[df_year["Conso totale (MWh)"] >= 1].copy()#on utilise que les valeurs >=1 pour éviter les valeurs négatives ou nulles dans le log
        df_log["log_conso"] = np.log10(df_log["Conso totale (MWh)"])
        

        fig = px.histogram(
            df_log,
            x="log_conso",
            nbins=50,#nombre de "slices" de l'histogramme
            title=f"Répartition en {selected_year}",
            hover_data={"log_conso": False, "Conso totale (MWh)": ":,.0f"}
        )

        #On veut des ticks personnalisés pour l'axe x (logarithmique)
        fig.update_xaxes(
            tickvals=np.arange(0, 7, 0.5),  # log10 : pas de 0.5
            ticktext=[
                "1 MWh", "3 MWh",
                "10 MWh", "30 MWh",
                "100 MWh", "300 MWh",
                "1 GWh", "3 GWh",
                "10 GWh", "30 GWh",
                "100 GWh", "300 GWh",
                "1 TWh"
            ],
            title="Consommation totale"
        )

        fig.update_yaxes(title="Nombre de communes")

        fig.update_traces(
            hovertemplate="<b>Consommation approx. :</b> 10^%{x:.1f} MWh<br>" + "Communes : %{y}<extra></extra>" #permet une lisibilité potable du log
        )

        fig.add_annotation(
            text=f"Communes à très faible consommation (<= 1 MWh) : {nb_tres_faible}",
            xref="paper",
            yref="paper",
            x=0.99,
            y=0.95,
            showarrow=False, #permet l'intégration dans le graphique sans flèche
            align="right"
        )

        return fig
# --- END CALLBACK ---