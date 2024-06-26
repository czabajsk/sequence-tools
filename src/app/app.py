"""
Web app
"""

import re  # regular expression operations
import logging
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd

from home_page import HOME_LAYOUT
from info_page import EXPLANATION_LAYOUT
from features.needleman_wunsch import (
    needleman_wunsch,
    initialise_grid,
    fill_scores,
    trace_through_alignment,
)

logger = logging.getLogger(__name__)

app = Dash(
    external_stylesheets=[dbc.themes.MINTY, dbc.themes.GRID],
    suppress_callback_exceptions=True,
)

# Navbar definition
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Algorithm", href="/")),
        dbc.NavItem(dbc.NavLink("Explanation", href="/explanation")),
    ],
    brand_href="/",
    color="info",
    dark=True,
    className="fixed-top w-100",
)

# Main layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),  # Tracks the URL
        navbar,
        html.Div(id="page-content"),  # Container for dynamic page content
    ]
)


def validate_sequence(sequence):
    """
    Validate that the sequence contains only letters and hyphens
    :param sequence: sequence to validate
    :return: boolean indicating if the sequence is valid
    """
    pattern = re.compile("^[A-Za-z-]*$")
    return bool(pattern.fullmatch(sequence))


@callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    """
    Callback to update the page content based on the URL
    :param pathname: requested sub-page
    :return: layout of one of the sub-pages
    """
    if pathname == "/explanation":
        return EXPLANATION_LAYOUT
    return HOME_LAYOUT  # Default to home


@callback(
    Output("body-div", "children"),
    [Input("generate_alignment", "n_clicks")],
    [
        State("seq_1", "value"),
        State("seq_2", "value"),
        State("match_score", "value"),
        State("mismatch_penalty", "value"),
        State("gap_penalty", "value"),
    ],
)
def generate_raw_alignment(
    n_clicks, seq_1, seq_2, match_score, mismatch_penalty, gap_penalty
):
    # pylint: disable=too-many-arguments
    """
    Display raw alignment
    :param n_clicks: button clicks
    :param seq_1: sequence one
    :param seq_2: sequence two
    :param match_score: match score
    :param mismatch_penalty: mismatch penalty
    :param gap_penalty: gap penalty
    :return: alignment with given or default parameters
    """
    if n_clicks is None or seq_1 is None or seq_2 is None:
        raise PreventUpdate

    if not validate_sequence(seq_1) or not validate_sequence(seq_2):
        return "Sequences can only contain letters and hyphens."

    # Use default values if any parameter is None
    match_score = match_score if match_score is not None else 1
    mismatch_penalty = mismatch_penalty if mismatch_penalty is not None else 1
    gap_penalty = gap_penalty if gap_penalty is not None else 1

    return needleman_wunsch(
        seq_1, seq_2, match=match_score, mismatch=mismatch_penalty, gap=gap_penalty
    )


@callback(
    Output("output-container", "children"),
    [Input("generate_alignment", "n_clicks")],
    [
        State("seq_1", "value"),
        State("seq_2", "value"),
        State("match_score", "value"),
        State("mismatch_penalty", "value"),
        State("gap_penalty", "value"),
    ],
)
def plot_score_table(
    n_clicks, seq_1, seq_2, match_score, mismatch_penalty, gap_penalty
) -> dash_table.DataTable:
    # pylint: disable=too-many-arguments
    """
    Plot scores
    :param n_clicks: button clicks
    :param seq_1: first sequence
    :param seq_2: second sequence
    :param match_score: match score
    :param mismatch_penalty: mismatch penalty
    :param gap_penalty: gap penalty
    :return: widget
    """
    if n_clicks is None or seq_1 is None or seq_2 is None:
        raise PreventUpdate

    if not validate_sequence(seq_1) or not validate_sequence(seq_2):
        return ""

    # Use default values if any parameter is None
    match_score = match_score if match_score is not None else 1
    mismatch_penalty = mismatch_penalty if mismatch_penalty is not None else 1
    gap_penalty = gap_penalty if gap_penalty is not None else 1

    scores_grid = initialise_grid(seq_1, seq_2, gap=gap_penalty)
    pointers_to_trace_optimal_alignment = fill_scores(
        scores_grid,
        seq_1,
        seq_2,
        gap=gap_penalty,
        match=match_score,
        mismatch=mismatch_penalty,
    )
    _, _, trace = trace_through_alignment(
        pointers_to_trace_optimal_alignment, seq_1, seq_2
    )
    logger.debug(trace)
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
        style_data_conditional=get_cell_styles(trace),
    )


def to_column_label(column_labels, column_in_df) -> str:
    """
    Necessary to keep labels consistent but ids of columns unique
    :param column_labels:
    :param column_in_df:
    :return:
    """
    if column_in_df in ["*", ""]:
        return column_in_df
    return column_labels[int(column_in_df)]


def get_cell_styles(matrix) -> list[dict]:
    """
    Generates styles for cells based on trace
    """
    red = "#EE6D80"
    result = [
        {
            "if": {"row_index": 0, "column_id": "0"},
            "backgroundColor": red,
            "color": "white",
        }
    ]
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            if value > 0:
                style = {
                    "if": {"row_index": row_index, "column_id": f"{col_index}"},
                    "backgroundColor": red if value > 1 else "#BDC1C7",
                    "color": "white",
                }
                result.append(style)

    return result


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8000", debug=True)
