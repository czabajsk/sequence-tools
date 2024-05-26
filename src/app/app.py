"""
Web app
"""

from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
from src.features.needleman_wunsch import needleman_wunsch, initialise_grid, fill_scores

app = Dash()

app.layout = [
    html.H1(children="Needleman-Wunsch Demo", style={"textAlign": "center"}),
    dcc.Input(placeholder="Sequence A", type="text", required=True, id="seq_1"),
    dcc.Input(placeholder="Sequence B", type="text", required=True, id="seq_2"),
    html.Button("Generate", id="generate_alignment"),
    html.Pre(id="body-div"),
    html.Div(id="default-alignment-viewer-output"),
    html.Div(id="output-container"),
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
    [State("seq_1", "value"), State("seq_2", "value")],
)
def plot_score_table(n_clicks, seq_1, seq_2):
    """
    Plot scores
    :param n_clicks: button clicks
    :param seq_1: first sequence
    :param seq_2: second sequence
    :return: widget
    """
    if n_clicks is None:
        raise PreventUpdate
    scores_grid = initialise_grid(seq_1, seq_2)
    pointers_to_trace_optimal_alignment = fill_scores(scores_grid, seq_1, seq_2)
    columns = list(seq_2)
    columns.insert(0, "")
    first_column = list(seq_1)
    first_column.insert(0, "")
    df = pd.DataFrame(data=pointers_to_trace_optimal_alignment)
    df.insert(loc=0, column="*", value=first_column)
    return dash_table.DataTable(
        df.to_dict("records"),
        [{"name": to_column_label(columns, i), "id": str(i)} for i in df.columns],
        id="tbl",
    )


def to_column_label(column_labels, column_in_df):
    """
    Necessary to keep labels consistent but ids of columns unique
    :param column_labels:
    :param column_in_df:
    :return:
    """
    if column_in_df in ["*", ""]:
        return column_in_df
    return column_labels[int(column_in_df)]


if __name__ == "__main__":
    app.run(debug=True)
