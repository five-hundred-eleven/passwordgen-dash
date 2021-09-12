import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from flask_app import app, server


navbar = dbc.NavbarSimple(
    brand="Password Generation",
    brand_href="/",
    children=[
        dbc.NavItem(dcc.Link("Generate a Password", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Generate a Passphrase", href="/passphrase", className="nav-link")),
    ],
    sticky="top",
    color="#511",
    light=False,
    dark=True,
)

default_layout = html.Div([])

layout = html.Div([
    html.Div(id="background-image"),
    html.Div([
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Row([
            dbc.Col(
                [],
                sm=0,
                md=2,
                className="buffer",
            ),
            dbc.Col(
                [
                    dcc.Markdown("""
                        ### Warning

                        This app has not been analyzed by security professionals so I
                        do not advise using it for sensitive purposes. If you like
                        it, clone it and run the server on a trusted local machine. See
                        [the source](https://github.com/ekoly/passwordgen-dash).
                    """, className="disclaimer"),
                    dbc.Container(id="page-content"),
                ],
                sm=12,
                md=6,
                className="main-area",
            ),
            dbc.Col(
                [],
                sm=0,
                md=4,
                className="buffer",
            ),

        ])
    ], id="content")
])

app.layout = layout

# nav callbacks

import password_app, passphrase_app

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"),],
)
def displayPage(path_name):
    if path_name == "/":
        return password_app.layout
    if path_name == "/passphrase":
        return passphrase_app.layout
    return default_layout

if __name__ == "__main__":
    app.run_server(debug=False)
