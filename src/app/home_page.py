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

    return dbc.Container(
        [
            html.Div(style={"height": "70px"}),  # Spacer
            html.H1(children="Needleman-Wunsch Demo", style={"textAlign": "center"}),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4(
                                        children="Sequences",
                                        style={"textAlign": "left"},
                                    ),
                                    dbc.Textarea(
                                        placeholder="Sequence A",
                                        size="lg",
                                        className="mb-4",
                                        required=True,
                                        id="seq_1",
                                        style={"resize": "none"},
                                    ),
                                    dbc.Textarea(
                                        placeholder="Sequence B",
                                        size="lg",
                                        className="mb-2",
                                        required=True,
                                        id="seq_2",
                                        style={"resize": "none"},
                                    ),
                                ]
                            )
                        ),
                        width=9,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4(
                                        children="Parameters",
                                        style={"textAlign": "left"},
                                    ),
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText(
                                                "Match Score", style={"width": "70%"}
                                            ),
                                            dbc.Input(
                                                placeholder="1",
                                                type="number",
                                                id="match_score",
                                                size="lg",
                                            ),
                                        ],
                                        className="mb-3 mt-3",
                                    ),
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText(
                                                "Mismatch Penalty",
                                                style={"width": "70%"},
                                            ),
                                            dbc.Input(
                                                placeholder="1",
                                                type="number",
                                                id="mismatch_penalty",
                                                size="lg",
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupText(
                                                "Gap Penalty", style={"width": "70%"}
                                            ),
                                            dbc.Input(
                                                placeholder="1",
                                                type="number",
                                                id="gap_penalty",
                                                size="lg",
                                            ),
                                        ],
                                        className="mb-1",
                                    ),
                                ]
                            ),
                            style={"width": "18rem"},
                        ),
                        width=3,
                    ),
                ]
            ),
            dbc.Button(
                "Generate",
                id="generate_alignment",
                color="info",
                size="lg",
                className="mt-3",
            ),
            html.Pre("(no content)", id="body-div", className="code mb-3 mt-3"),
            html.Div(id="default-alignment-viewer-output"),
            html.Div(id="output-container"),
        ],
        fluid=True,
    )


HOME_LAYOUT = create_home_layout()
