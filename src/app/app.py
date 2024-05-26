"""
Web app
"""
from dash import Dash, html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bio as dashbio
from src.features.needleman_wunsch import needleman_wunsch

app = Dash()

app.layout = [
    html.H1(children="Needleman-Wunsch Demo", style={"textAlign": "center"}),
    dcc.Input(placeholder="Sequence A", type="text", required=True, id="seq_1"),
    dcc.Input(placeholder="Sequence B", type="text", required=True, id="seq_2"),
    html.Button("Generate", id="generate_alignment"),
    html.Pre(id="body-div"),
    html.Div(id='default-alignment-viewer-output'),
    html.Div(id="output-container")
]


@callback(
    Output("body-div", "children"),
    [Input("generate_alignment", "n_clicks")],
    [State("seq_1", "value"), State("seq_2", "value")],
)
def generate_raw_alignment(n_clicks, seq_1, seq_2):
    """
    Display raw alignment
    :param n_clicks: button clicks
    :param seq_1: sequence one
    :param seq_2: sequence two
    :return: alignment with default parameters
    """
    if n_clicks is None:
        raise PreventUpdate
    return needleman_wunsch(seq_1, seq_2)

@callback(
    Output("output-container", "children"),
    [Input("generate_alignment", "n_clicks")],
    [State("seq_1", "value"),
     State("seq_2", "value")],
)
def plot_alignment_chart(n_clicks, seq_1, seq_2):
    """
    Plot interactive chart
    :param n_clicks: button clicks
    :param seq_1: first sequence
    :param seq_2: second sequence
    :return: widget
    """
    if n_clicks is None:
        return 'No data.'
    data = f""">SEQUENCE_1
{seq_1}
>SEQUENCE_2
{seq_2}"""

    return dashbio.AlignmentChart(
        id='my-default-alignment-viewer',
        data=data,
        showconservation=False,
        height=500,
        tilewidth=30,
    )


if __name__ == "__main__":
    app.run(debug=True)
