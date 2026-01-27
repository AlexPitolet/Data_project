from dash import html, dcc, Input, Output
from src.component import header

layout = html.Div(
    [
        html.H2("Carte magique"),
        html.P("Ce dashboard met en évidence les disparités de consommation électrique entres les région et les départements en fFrance de 2011 à 2024")
    ]
)