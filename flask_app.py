import os
from flask import Flask, send_from_directory


FLASK_APP = Flask(__name__)

@FLASK_APP.route("/js/<filename>")
def static_js(filename):
    """
        Serves javascript files.
    """
    path = os.path.join(os.getcwd(), "js")
    return send_from_directory(path, filename)

@FLASK_APP.route("/css/<filename>")
def static_css(filename):
    """
        Serves css files.
    """
    path = os.path.join(os.getcwd(), "css")
    return send_from_directory(path, filename)
