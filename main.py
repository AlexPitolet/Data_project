import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

from src.component.header import header
from src.component.footer import footer
from src.component.navbar import navbar
from src.pages import home

def main():
    app = Dash(__name__)

    app.layout = html.Div([
        dcc.Location(id="url"),
        header(),
        navbar(),
        html.Div(id="page-content"),
        footer()
    ],
    style={"font-family":"Arial, sans-serif","text-align":"center"}
    )
    app.run(debug=True)
    @app.callback(
        Output("page-content","children"),
        Input("url","pathname")
    )
    def display_page(pathname):
        if(pathname in ["/","/home"]):
            return home.layout


if __name__ == "__main__":
    main()
