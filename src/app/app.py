"""
Web app
"""
from dash import Dash, html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate
from src.features.needleman_wunsch import needleman_wunsch

app = Dash()

app.layout = [
    html.H1(children="Needleman-Wunsch Demo", style={"textAlign": "center"}),
    dcc.Input(placeholder="Sequence A", type="text", required=True, id="seq_1"),
    dcc.Input(placeholder="Sequence B", type="text", required=True, id="seq_2"),
    html.Button("Generate", id="generate_alignment"),
    html.Pre(id="body-div"),
]


@callback(
    Output("body-div", "children"),
    [Input("generate_alignment", "n_clicks")],
    [State("seq_1", "value"), State("seq_2", "value")],
)
def update_graph(n_clicks, seq_1, seq_2):
    """
    Display raw alignment
    :param n_clicks: button click
    :param seq_1: sequence one
    :param seq_2: sequence two
    :return: alignment with default parameters
    """
    if n_clicks is None:
        raise PreventUpdate
    return needleman_wunsch(seq_1, seq_2)


if __name__ == "__main__":
    app.run(debug=True)
