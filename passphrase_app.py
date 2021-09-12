import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from password_generation import generatePassphrase

from flask_app import app


DEFAULT_PASSPHRASE_LENGTH = 5


layout = (
    html.Div([
        dcc.Markdown("""
            # Generate a Random Word Passphrase

            This will grab a random wikipedia article and select random words from the
            article, seperated by a random special character, to use as a passphrase.
            Some security experts [believe that passphrases are harder to guess and
            easier to remember than passwords](https://protonmail.com/blog/protonmail-com-blog-password-vs-passphrase/).
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
    ])
)

# passphrase callbacks

@app.callback(
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

@app.callback(
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

