from dash import html, dcc

def navbar():
    return html.Nav([
        dcc.Link("Accueil", href="/home"),
        dcc.Link("Carte", href="/map"),
        dcc.Link("Histogramme", href="/hist"),
        dcc.Link("Graphique dynamique", href="/dynamic-graph"),
        dcc.Link("À propos", href="/about")
    ],
    style={
        "padding":"1em",
        "backgroundColor":"#eee",
        "display":"flex",
        "justify-content":"space-evenly"
    }
    )