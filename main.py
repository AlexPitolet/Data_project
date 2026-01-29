import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

from src.component.header import header
from src.component.footer import footer
from src.component.navbar import navbar
from src.pages import home,map,hist,dynamic,about

def main():
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
