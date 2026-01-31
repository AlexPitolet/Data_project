from dash import html, dcc, Input, Output
from src.component import header

layout = html.Div(
    [
        html.H2("Explorer la consommation électrique en France"),
        html.P("Ce dashboard met en évidence les disparités de consommation d'énergie (électricité et gaz) en France de 2011 à 2024\n"),
        html.P("Les données sont disponibles à l’échelle régionale et départementale, afin de mettre en évidence les disparités territoriales.\n"),
        html.P("Vous pourrez découvrir :"),
        html.Ul(
            [
                html.Li("Une carte interactive afin d'identifier clairement les disparité géographique"),
                html.Li("Un histogramme catégoriel reportant la consommation moyenne par régions"),
                html.Li("Un histogramme non catégoriel dynamique permettant de visualiser l'évolution de la consommation moyenne en fonction du nombre d'habitants")
            ]
        ),
        html.P(
            "Utilisez le menu de navigation pour explorer les différentes visualisations."
        ),
    ],
    style={
        "margin":"auto",
        "width":"50vw",
        "textAlign": "justify"
    }
)