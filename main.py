
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

from src.component.header import header
from src.component.footer import footer
from src.component.navbar import navbar

from src.utils.clean_data import clean_all_data
import src.utils.get_data as gd   
from src.utils.get_data import get_data, get_geojson, get_csv, get_all_data

if __name__ == '__main__':
    gd.get_all_data()   # verify that the data is present
    clean_all_data()    # verify is rawdata as been cleaned. Keeping only useful data to lighten the dashboard
    from src.pages import home,map,non_cat_hist,dynamic_hist,about # import après le nettoyage des données car map.py à besoin des données 

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
        if(pathname in ["/non_cat_hist"]):
            return non_cat_hist.layout
        if(pathname in ["/dynamic_hist"]):
            return dynamic_hist.layout
        if(pathname in ["/about"]):
            return about.layout
        
        return html.H1("404 - Page non trouvée")
    map.register_callback(app)
    non_cat_hist.register_callback(app)
    dynamic_hist.register_callback(app)

    app.run(debug=True)
