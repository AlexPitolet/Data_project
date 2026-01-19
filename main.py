
#
# Imports
#
import numpy as np
import pandas as pd
import plotly.express as px

import dash
from dash import Dash,dcc,html
from dash.dependencies import Input,Output

#
# Data
#

df = pd.read_csv("data/cleaned/conso_per_region.csv")

#
# Main
#

def main():
    app = dash.Dash(__name__) # (3)

    fig = px.bar(df, x="Nom Région", y="Conso moyenne (MWh)", color="Nom Région") # (4)


    app.layout = html.Div(children=[

                            html.H1(children=f'Conso per region ',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                            html.Div(children=f'''
                                Ce graphe montre la consommation moyenne d'électricité en MWh par 
                                région, lissée par nombre de site pt de livraison) au sein de cette dernière.
                                Chaque région possède sa couleur et la taille d'une barre dans l'histogramme
                                est proportionnelle à la consommation de la région associée
                                Passe la souris par dessus pour plus de détail.
                            '''), # (7)

    ]
    )

    #
    # RUN APP
    #

    app.run(debug=True) # (8)

if __name__ == '__main__':
    main()