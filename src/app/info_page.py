"""
Page 2 layout: Explanation of the algorithm
"""
from dash import html
import dash_bootstrap_components as dbc


def create_how_it_works_section() -> list:
    """
    Returns 'How it works?' section
    :return: list with html elements
    """
    return [
        html.H3("""
        1. To run the Needleman-Wunsch algorithm, two sequences of characters need to be provided
           along with default values for match, mismatch, and gap, where:"""),
        html.Ul([
            html.Li("""
            match/mismatch: value 
            for a correct match or mismatch between characters"""),
            html.Li("""
            gap: represents the penalty 
            for introducing a gap (or a space) in the sequence"""),
        ]),
        html.H3("2. Creating initial matrix"),
        html.P("""
            Constructing a scores matrix, that ultimately stores the optimal score 
            at each possible pair of characters. The first row and the first column 
            is filled by subtracting the size of penalty (gap) starting from 0."""),
        html.Pre(children=[
            html.Code("""
        scores[i][0] = -i * gap for i = 1, 2, ..., m
        scores[0][j] = -j * gap for j = 1, 2, ..., n""")
        ],
            className="code"),
        html.H3("3. Calculating values in the result matrix:"),
        html.Div([
            html.P("""
                If sequence one is represented as X and sequence two as Y,
                then the matrix is filled based on the formula:"""),
            html.Pre(children=[
                html.Code("""
        scores[i][j] = max{
            scores[i-1][j-1] + match/mismatch if X[i] = Y[j],
            scores[i-1][j] - gap for gap in sequence X,
            scores[i][j-1] - gap for gap in sequence Y
        }""")
            ],
                className="code")
        ]),
        html.H3("4. Fill the scores"),
        html.P("""
        The traceback matrix is filled, storing information about the operation that resulted in choosing 
        the optimal score at each possible pair of characters. Based on the formula provided above, 
        we have three possible outcomes. The matrix is filled with points depending on whether a match/mismatch, 
        a gap in sequence X, or a gap in sequence Y was used."""),
        html.H3("5. Tracing back the best alignment"),
        html.P("""
        The results are traced backward (starting from the end of the matrix) - thanks to filling the matrix 
        'pointers_to_trace_optimal_alignment' in the previous step, the algorithm knows the operation that led 
        to the alignment, and this is information about which field to move to. The result of this process 
        is a two sequences of characters, representing the best alignment with each other."""),
    ]


def create_about_section() -> list:
    """
    Returns about section
    :return: list of html elements
    """
    return [
        html.P(
            [
                "The ",
                html.A("Needleman-Wunsch algorithm",
                       href="https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm",
                       target="_blank"),  # directs to wikipedia
                """
                , developed by Saul B. Needleman and Christian D. Wunsch and published in 1970,
                is a widely utilized tool in bioinformatics for aligning protein 
                or nucleotide sequences. It stands as one of the pioneering applications of 
                dynamic programming in comparing biological sequences. Beyond its origins in 
                bioinformatics, this algorithm finds extensive application across various 
                domains due to its versatility in comparing any two sequences of characters."""]
        )
    ]


def create_explanation_layout() -> dbc.Container:
    """
    Creates info page layout
    :return: dbc.Container
    """
    return dbc.Container([
        dbc.Row(dbc.Col(html.H2("About"), width={"size": 6, "offset": 3}),
                align="center"),
        dbc.Row(dbc.Col(create_about_section(), width={"size": 8, "offset": 2}),
                align="center"),
        dbc.Row(dbc.Col(html.H2("How it works"), width={"size": 6, "offset": 3}),
                align="center"),
        dbc.Row(dbc.Col(create_how_it_works_section(), width={"size": 8, "offset": 2}),
                align="center"),
    ],
        fluid=True)


EXPLANATION_LAYOUT = create_explanation_layout()
