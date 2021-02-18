from flask import Flask, render_template, request
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from PasswordGeneration import generatePassword 

DEFAULT_PASSWORD_LENGTH = 18


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
]

meta_tags = [
    {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }
]

FLASK_APP = Flask(__name__)
APP = Dash(__name__, server=FLASK_APP, meta_tags=meta_tags, external_stylesheets=external_stylesheets)

layout = html.Div([
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
                    # Generate a Password

                    Generate an easy-to-type and readable random password.

                    Practice entering the password in the input box below the generated password.
                    
                    See [the source](https://github.com/ekoly/passwordgen-dash).
                """),
                html.Div([], id="length-indicator"),
                dcc.RangeSlider(
                    id="password-length",
                    min=5,
                    max=80,
                    step=1,
                    value=[DEFAULT_PASSWORD_LENGTH,],
                ),
                html.Div([], id="generated-password"),
                dcc.Input(id="confirm-password", style={"width": "100%"}),
                html.Div([], id="confirm-password-indicator"),
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
])

APP.layout = layout


current_generated_password = ""

@APP.callback(
    [
        Output("generated-password", "children"),
        Output("length-indicator", "children"),
        Output("confirm-password", "value"),
    ],
    [
        Input("password-length", "value"),
    ],
)
def updateGeneratedPassword(num_letters):
    """
        Update the generated password.
    """

    global current_generated_password

    num_letters, = num_letters

    print(f"Number of letters selected: {num_letters}")

    indicator_text = f"""
        Select length with the slider: {num_letters}
    """
    current_generated_password = generatePassword(int(num_letters))
    return (
        dcc.Markdown(current_generated_password),
        dcc.Markdown(indicator_text),
        "",
    )

@APP.callback(
    Output("confirm-password-indicator", "children"),
    [
        Input("confirm-password", "value"),
        Input("password-length", "value"),
    ]
)
def confirmPassword(entered_password, *args):
    """
        User practices entering the password.
    """

    global current_generated_password

    print(f"generated password: {current_generated_password}")
    print(f"entered password:   {entered_password}")

    if entered_password == current_generated_password:
        return dcc.Markdown("Correct!", style={"color": "green"})
    elif entered_password == "":
        return dcc.Markdown("try typing the password!")
    else:
        return dcc.Markdown("Wrong!", style={"color": "red"})


if __name__ == "__main__":
    APP.run_server(debug=True)
