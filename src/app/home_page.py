"""
Page 1 layout: Needleman-Wunsch algorithm input
"""

from dash import html
import dash_bootstrap_components as dbc


def create_home_layout() -> dbc.Container:
    """
    Returns home page layout
    :return: dbc.Container
    """
    
    return dbc.Container([
        html.Div(style={"height": "70px"}),  # Spacer
        html.H1(children="Needleman-Wunsch Demo", style={"textAlign": "center"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(
                            placeholder="Sequence A",
                            type="text",
                            size="lg",
                            className="mb-3",
                            required=True,
                            id="seq_1",
                        ),
                        dbc.Input(
                            placeholder="Sequence B",
                            type="text",
                            size="lg",
                            className="mb-3",
                            required=True,
                            id="seq_2",
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Input(
                            placeholder="Match Score (default: 1)",
                            type="number",
                            size="lg",
                            className="mb-3",
                            id="match_score",
                        ),
                        dbc.Input(
                            placeholder="Mismatch Penalty (default: 1)",
                            type="number",
                            size="lg",
                            className="mb-3",
                            id="mismatch_penalty",
                        ),
                        dbc.Input(
                            placeholder="Gap Penalty (default: 1)",
                            type="number",
                            size="lg",
                            className="mb-3",
                            id="gap_penalty",
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
        dbc.Button("Generate", id="generate_alignment", color="info", size="lg"),
        html.Pre("(no content)", id="body-div", className="code mb-3 mt-3"),
        html.Div(id="default-alignment-viewer-output"),
        html.Div(id="output-container"),
    ],
        fluid=True,
    )


HOME_LAYOUT = create_home_layout()

