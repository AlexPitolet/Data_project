from dash import html

def navbar():
    return html.Nav([
        html.P("Carte"),
        html.P("Histogramme"),
        html.P("Graphique dynamique"),
        html.P("À propos")
    ],style={"display":"flex",
             "justify-content":"space-evenly"
             }
    )