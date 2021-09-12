from dash import Dash
import dash_bootstrap_components as dbc
from flask import Flask, send_from_directory
import os

server = Flask(__name__)

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "/css/main.css",
]

meta_tags = [
    {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }
]

app = Dash(__name__, server=server, meta_tags=meta_tags, external_stylesheets=external_stylesheets)

@server.route("/js/<filename>")
def static_js(filename):
    """
        Serves javascript files.
    """
    path = os.path.join(os.getcwd(), "js")
    return send_from_directory(path, filename)

@server.route("/css/<filename>")
def static_css(filename):
    """
        Serves css files.
    """
    path = os.path.join(os.getcwd(), "css")
    return send_from_directory(path, filename)

@server.route("/img/<filename>")
def static_img(filename):
    """
        Serves image files.
    """
    path = os.path.join(os.getcwd(), "img")
    return send_from_directory(path, filename)
