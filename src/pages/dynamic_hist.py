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


                        html.Div(children=f'''
                            Ce graphe montre la consommation moyenne d'électricité en MWh par 
                            région, lissée par nombre de site pt de livraison) au sein de cette dernière.
                            Chaque région possède sa couleur et la taille d'une barre dans l'histogramme
                            est proportionnelle à la consommation de la région associée
                            Passe la souris par dessus pour plus de détail.
                        '''), 

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