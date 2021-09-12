import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from flask_app import app
from password_generation import generatePassword


DEFAULT_PASSWORD_LENGTH = 15


layout = (
    html.Div([
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
            ### What do "easy to type" and "easy to read" mean?

            "Easy to type" means:
            * Alternating between keys typed by the left hand and right hand
            * Avoiding keys that require moving the hands too far away from the home row
            * If the previous letter required the Shift key, the next letter will not use
            the pinky finger (and vice versa)

            "Easy to read" simply means avoiding letters that are easily mistaken for other
            letters, such as 1/l, 0/O, etc.
        """),
    ])
)

# password callbacks

@app.callback(
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

@app.callback(
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

