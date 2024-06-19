"""
Web app
"""
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
from src.features.needleman_wunsch import (
    needleman_wunsch,
    initialise_grid,
    fill_scores,
    trace_through_alignment,
)
app = Dash(external_stylesheets=[dbc.themes.MINTY], suppress_callback_exceptions=True)
#app = Dash()

# Navbar definition
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Algorithm", href="/")),
        dbc.NavItem(dbc.NavLink("Explanation", href="/explanation")),
    ],
    brand_href="/",
    color="info",
    dark=True,
    className="fixed-top w-100"
)

# Page 1 layout: Needleman-Wunsch algorithm input
home_layout = dbc.Container([
    html.Div(style={"height": "70px"}),  # Spacer
    html.H1(children="Needleman-Wunsch Demo", style={"textAlign": "center"}),
    dbc.Input(placeholder="Sequence A", type="text", size="lg", className="mb-3", required=True, id="seq_1"),
    dbc.Input(placeholder="Sequence B", type="text", size="lg", className="mb-3", required=True, id="seq_2"),
    dbc.Button("Generate", id="generate_alignment", color="info", size="lg"),
    html.Pre(id="body-div"),
    html.Div(id="default-alignment-viewer-output"),
    html.Div(id="output-container"),
], fluid=True)

# Page 2 layout: Explanation of the algorithm
explanation_layout = dbc.Container([
    html.Div(style={"height": "70px"}),  # Spacer
    html.P([
        "The ",
        html.A("Needleman-Wunsch algorithm", href="https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm",
               target="_blank"), # directs to wikipedia
        ", developed by Saul B. Needleman and Christian D. Wunsch and published in 1970, is a widely utilized tool in bioinformatics for aligning protein or nucleotide sequences. It stands as one of the pioneering applications of dynamic programming in comparing biological sequences. Beyond its origins in bioinformatics, this algorithm finds extensive application across various domains due to its versatility in comparing any two sequences of characters."
    ], style={"fontSize": "26px", "margin-top": "150px"}),
    html.H2("How it works?"),
    html.Div([
    html.H3("1. To run the Needleman-Wunsch algorithm, two sequences of characters need to be provided along with default values for match, mismatch, and gap, where:"),
    html.Ul([
        html.Li("match/mismatch: value for a correct match or mismatch between characters"),
        html.Li("gap: represents the penalty for introducing a gap (or a space) in the sequence"),
    ]),
    html.H3("2. Creating initial matrix"),
    html.P("""
        Constructing a scores matrix, that ultimately stores the optimal score at each possible pair of characters. 
        The first row and the first column is filled by subtracting the size of penalty (gap) starting from 0.
    """),
    html.Pre(children=[
        html.Code("""
    scores[i][0] = -i * gap for i = 1, 2, ..., m
    scores[0][j] = -j * gap for j = 1, 2, ..., n
            """)
    ]),
    html.H3("3. Calculating values in the result matrix:"),
    html.Div([
        html.P(
            "If sequence one is represented as X and sequence two as Y, then the matrix is filled based on the formula:"),
        html.Pre(children=[
            html.Code("""
    scores[i][j] = max{
        scores[i-1][j-1] + match/mismatch if X[i] = Y[j],
        scores[i-1][j] - gap for gap in sequence X,
        scores[i][j-1] - gap for gap in sequence Y
    }
                """)
        ])
    ]),
    html.H3("4. Fill the scores"),
    html.P("""
        The traceback matrix is filled, storing information about the operation that resulted in choosing the optimal score 
        at each possible pair of characters. Based on the formula provided above, we have three possible outcomes. The matrix 
        is filled with points depending on whether a match/mismatch, a gap in sequence X, or a gap in sequence Y was used.
    """),
    html.H3("5. Tracing back the best alignment"),
    html.P("""
        The results are traced backward (starting from the end of the matrix) - thanks to filling the matrix 'pointers_to_trace_optimal_alignment' 
        in the previous step, the algorithm knows the operation that led to the alignment, and this is information about which field to move to. 
        The result of this process is a two sequences of characters, representing the best alignment with each other.
    """),
], className="content-with-margins")  # Zastosowanie klasy CSS do zwiększenia marginesów
], fluid=True)
# Main layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Tracks the URL
    navbar,
    html.Div(id='page-content')  # Container for dynamic page content
])

# Callback to update the page content based on the URL
@callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/explanation':
        return explanation_layout
    else:
        return home_layout  # Default to home

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
    _, _, trace = trace_through_alignment(
        pointers_to_trace_optimal_alignment, seq_1, seq_2
    )
    print(trace)
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


def get_cell_styles(matrix):
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
    app.run(debug=True)
