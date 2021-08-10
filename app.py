from flask import Flask
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from flask_app import FLASK_APP
from password_generation import generatePassword, generatePassphrase 

DEFAULT_PASSWORD_LENGTH = 15
DEFAULT_PASSPHRASE_LENGTH = 5


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "/css/main.css",
]

#  external_scripts = [
    #  "/js/confirm_password.js",
#  ]

meta_tags = [
    {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }
]

APP = Dash(__name__, server=FLASK_APP, meta_tags=meta_tags, external_stylesheets=external_stylesheets)

layout = html.Div([
    html.Div(id="background-image"),
    html.Div([
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

                        Security was not taken into consideration in this app so I
                        do not advise using it for sensitive purposes. If you like
                        it, clone it and run the server on a trusted local machine. See
                        [the source](https://github.com/ekoly/passwordgen-dash).
                    """, className="disclaimer"),
                    dcc.Markdown("""
                        # Generate a Random Character Password

                        Generate an easy-to-type and readable random character password.
                    """),
                    html.Div([], id="length-indicator"),
                    dcc.Slider(
                        id="password-length",
                        min=5,
                        max=80,
                        step=1,
                        value=DEFAULT_PASSWORD_LENGTH,
                    ),
                    html.Button("Generate Another", id="generate-another"),
                    html.Div([], id="generated-password"),
                    dcc.Input(
                        id="confirm-password",
                        spellCheck=False,
                        autoComplete="off",
                    ),
                    html.Div([], id="confirm-password-indicator"),
                    dcc.Markdown("""
                        ### What does "easy to type" and "easy to read" mean?

                        "Easy to type" means:
                        * Alternating between keys typed by the left hand and right hand
                        * Avoiding keys that require moving the hands too far away from the home row
                        * If the previous letter required the Shift key, the next letter will not use
                        the pinky finger (and vice versa)

                        "Easy to read" simply means avoiding letters that are easily mistaken for other
                        letters, such as 1/l, 0/O, etc.
                    """),
                    dcc.Markdown("""
                        # Generate a Random Word Passphrase

                        This will grab a random wikipedia article and select random words from the
                        article, seperated by a random special character, to use as a passphrase.
                        **The resulting password may contain offensive or NSFW words.** Some security
                        experts [believe that passphrases are harder to guess and easier to
                        remember than passwords](https://protonmail.com/blog/protonmail-com-blog-password-vs-passphrase/).
                    """),
                    html.Div([], id="length-indicator2"),
                    dcc.Slider(
                        id="passphrase-length",
                        min=4,
                        max=10,
                        step=1,
                        value=DEFAULT_PASSPHRASE_LENGTH,
                    ),
                    html.Button("Generate Another", id="generate-another2"),
                    html.Div([], id="generated-passphrase"),
                    dcc.Input(
                        id="confirm-passphrase",
                        spellCheck=False,
                        autoComplete="off",
                    ),
                    html.Div([], id="confirm-passphrase-indicator"),
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

APP.layout = layout

# password callbacks

@APP.callback(
    (
        Output("generated-password", "children"),
        Output("length-indicator", "children"),
        Output("confirm-password", "value"),
    ),
    (
        Input("password-length", "value"),
        Input("generate-another", "n_clicks"),
    ),
)
def updateGeneratedPassword(num_letters, *args):
    """
        Update the generated password.
    """

    indicator_text = f"""
        Select length with the slider: {num_letters}
    """
    current_generated_password = generatePassword(int(num_letters))
    return (
        current_generated_password,
        dcc.Markdown(indicator_text),
        "",
    )

@APP.callback(
    (
        Output("confirm-password-indicator", "children"),
        Output("confirm-password", "className"),
    ),
    (
        Input("confirm-password", "value"),
        Input("generated-password", "children"),
    )
)
def confirmPassword(entered_password, generated_password):
    """
        User practices entering the password.
    """

    if entered_password == generated_password:
        return (
            dcc.Markdown("correct!"),
            "affirm",
        )
    elif entered_password == "":
        return (
            dcc.Markdown("try typing the password!"),
            "",
        )
    else:
        return (
            dcc.Markdown("wrong!"),
            "scold",
        )

# passphrase callbacks

@APP.callback(
    (
        Output("generated-passphrase", "children"),
        Output("length-indicator2", "children"),
        Output("confirm-passphrase", "value"),
    ),
    (
        Input("passphrase-length", "value"),
        Input("generate-another2", "n_clicks"),
    ),
)
def updateGeneratedPassphrase(num_words, *args):
    """
        Update the generated password.
    """
    #print(f"Number of letters selected: {num_letters}")

    indicator_text = f"""
        Select number of words with the slider: {num_words}
    """
    current_generated_password = generatePassphrase(int(num_words))
    return (
        current_generated_password,
        dcc.Markdown(indicator_text),
        "",
    )

@APP.callback(
    (
        Output("confirm-passphrase-indicator", "children"),
        Output("confirm-passphrase", "className"),
    ),
    (
        Input("confirm-passphrase", "value"),
        Input("generated-passphrase", "children"),
    )
)
def confirmPassphrase(entered_passphrase, generated_passphrase):
    """
        User practices entering the passphrase.
    """

    if entered_passphrase == generated_passphrase:
        return (
            dcc.Markdown("correct!"),
            "affirm",
        )
    elif entered_passphrase == "":
        return (
            dcc.Markdown("try typing the passphrase!"),
            "",
        )
    else:
        return (
            dcc.Markdown("wrong!"),
            "scold",
        )


if __name__ == "__main__":
    APP.run_server(debug=True)
