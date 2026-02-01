import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output


df = pd.read_csv("data/cleaned/conso_totale.csv")
#df["Année"] = df["Année"].astype(int)
print(df[df["Année"] == 2019]["Code Commune"].nunique())
print(df["Code Commune"].nunique())


annees_disponibles = sorted(df["Année"].unique())
df_hist = df[["Code Commune", "Conso totale (MWh)", "Année"]]


layout = html.Div(children=[

                        html.H1(children=f"Distribution de la consommation totale d'électricité des communes",
                                    style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

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
                            #figure=fig
                        ), # (6)

                        html.Div(children=f'''
                            Ce graphe montre la distribution de la consommation totale d’électricité (en MWh) des communes françaises.
                            Chaque barre de l’histogramme représente un intervalle de valeurs de consommation, et sa hauteur correspond au nombre de communes dont la consommation se situe dans cet intervalle.

                            L’axe horizontal indique les classes de consommation, tandis que l’axe vertical traduit la fréquence des communes associées à chaque classe.
                            Ce type de représentation permet d’analyser la répartition globale des consommations, de mettre en évidence une éventuelle asymétrie, ainsi que la présence de communes fortement consommatrices par rapport à la majorité.

                            Passe la souris sur les barres pour obtenir des informations détaillées sur chaque intervalle.
                        '''), # (7)

]
)

def register_callback(app):
# --- CALLBACK ---
    @app.callback(
        Output('non_cat_hist', 'figure'),
        Input('year-slider-hist', 'value')
    )
    def update_figure(selected_year):

        df_year = df_hist[df_hist["Année"] == selected_year]
        df_year = df_year[df_year["Conso totale (MWh)"] > 0]
        df_tres_faible = df_year[df_year["Conso totale (MWh)"] < 1]
        
        nb_tres_faible = df_tres_faible["Code Commune"].nunique()

        df_log = df_year[df_year["Conso totale (MWh)"] >= 1]
        df_log["log_conso"] = np.log10(df_log["Conso totale (MWh)"])

        

        
        

        
        

        fig = px.histogram(
            df_log,
            x="log_conso",
            nbins=50,
            title=f"Répartition en {selected_year}"
        )

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
            hovertemplate=
            "Consommation : %{x:.1f} log10(MWh)<br>" +
            "Communes : %{y}<extra></extra>"
        )

        fig.add_annotation(
            text=f"Communes à très faible consommation (< 1 MWh) : {nb_tres_faible}",
            xref="paper",
            yref="paper",
            x=0.99,
            y=0.95,
            showarrow=False,
            align="right"
        )

        return fig
# --- END CALLBACK ---