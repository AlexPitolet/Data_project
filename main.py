
#
# Imports
#
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

from src.component.header import header
from src.component.footer import footer
from src.component.navbar import navbar

import dash
from dash import Dash,dcc,html
from dash.dependencies import Input,Output

from src.utils.get_data import get_all_data
from src.utils.clean_data import clean_all_data

'''
#
# Data
#

df = pd.read_csv("data/cleaned/conso_per_region.csv")
annees_disponibles = sorted(df['Année'].unique())
#
# Main
#

def main():
##################### MAIN ALEX ####################
    app = dash.Dash(__name__) # (3)

    #fig = px.bar(df, x="Nom Région", y="Conso moyenne (MWh)", color="Nom Région") # (4)


    app.layout = html.Div(children=[

                            html.H1(children=f'Conso per region ',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            #Year Slider
                            html.Div([
                                html.Label("Sélectionnez l'année :"),
                                dcc.Slider(
                                    id='year-slider',
                                    min=min(annees_disponibles),
                                    max=max(annees_disponibles),
                                    value=min(annees_disponibles), # Valeur par défaut
                                    marks={str(year): str(year) for year in annees_disponibles},
                                    step=None # Permet de ne cliquer que sur les années existantes
                                ),
                            ], style={'padding': '20px'}),

                            dcc.Graph(
                                id='graphConso',
                                #figure=fig
                            ), # (6)

                            html.Div(children=f"""
                                Ce graphe montre la consommation moyenne d'électricité en MWh par 
                                région, lissée par nombre de site pt de livraison) au sein de cette dernière.
                                Chaque région possède sa couleur et la taille d'une barre dans l'histogramme
                                est proportionnelle à la consommation de la région associée
                                Passe la souris par dessus pour plus de détail.
                            """), # (7)

    ]
    )

    # --- CALLBACK ---
    @app.callback(
        Output('graphConso', 'figure'),
        Input('year-slider', 'value')
    )
    def update_figure(selected_year):
        # 1. Filtrer le dataframe selon l'année choisie
        filtered_df = df[df['Année'] == selected_year]
        
        # 2. Créer la figure mise à jour
        fig = px.bar(
            filtered_df, 
            x="Nom Région", 
            y="Conso moyenne (MWh)", 
            color="Nom Région",
            title=f"Consommation en {selected_year}",
            range_y=[0, df["Conso moyenne (MWh)"].max() * 1.1] # Garder une échelle Y fixe
        )
    
        # Cosmétique
        fig.update_layout(transition_duration=500)
        
        return fig

    #
    # RUN APP
    #

    app.run(debug=True) # (8)
''' 
##################### MAIN ANTOINE ####################
def main():
    get_all_data() # verify that the data is present
    clean_all_data() # verify is rawdata as been cleaned. Keeping only useful data to lighten the dashboard
    
    from src.pages import home,map,hist,dynamic,about # import après le nettoyage des données car map.py à besoin des données 


    app = Dash(__name__,suppress_callback_exceptions=True)
    

    app.layout = html.Div([
        dcc.Location(id="url"),
        header(),
        navbar(),
        html.Div(id="page-content"),
        footer()
    ],
    style={"font-family":"Arial, sans-serif","text-align":"center"}
    )
    @app.callback(
        Output("page-content","children"),
        Input("url","pathname")
    )
    def display_page(pathname):
        if(pathname in ["/","/home"]):
            return home.layout
        if(pathname in ["/map"]):
            return map.layout
        if(pathname in ["/hist"]):
            return hist.layout
        if(pathname in ["/dynamic-graph"]):
            return dynamic.layout
        if(pathname in ["/about"]):
            return about.layout
        
        return html.H1("404 - Page non trouvée")
    map.register_callback(app)

    app.run(debug=True)

if __name__ == "__main__":
    main()
