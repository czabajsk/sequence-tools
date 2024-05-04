#!/usr/bin/env python
"""
The Needleman-Wunsch Algorithm
"""

import numpy as np


def needleman_wunsch(sequence_one: str, sequence_two: str, match=1, mismatch=1, gap=1):
    """
    :param sequence_one: First sequence
    :param sequence_two: Second sequence
    :param match: success score in case of character match
    :param mismatch: penalty value for each mismatch
    :param gap: penalty value for each gap
    :return: String with the pairwise sequence alignment
    """
    grid_x_dimension = len(sequence_one)
    grid_y_dimension = len(sequence_two)
    # Optimal score at each possible pair of characters.
    scores_grid = initialise_grid(gap, grid_x_dimension, grid_y_dimension)
    # Pointers to trace through an optimal alignment.
    pointers_to_trace_optimal_alignment = np.zeros((grid_x_dimension + 1, grid_y_dimension + 1))
    pointers_to_trace_optimal_alignment[:, 0] = 3
    pointers_to_trace_optimal_alignment[0, :] = 4
    temporary_scores = np.zeros(3)
    for i in range(grid_x_dimension):
        for j in range(grid_y_dimension):
            if sequence_one[i] == sequence_two[j]:
                temporary_scores[0] = scores_grid[i, j] + match
            else:
                temporary_scores[0] = scores_grid[i, j] - mismatch
            temporary_scores[1] = scores_grid[i, j + 1] - gap
            temporary_scores[2] = scores_grid[i + 1, j] - gap
            tmax = np.max(temporary_scores)
            scores_grid[i + 1, j + 1] = tmax
            if temporary_scores[0] == tmax:
                pointers_to_trace_optimal_alignment[i + 1, j + 1] += 2
            if temporary_scores[1] == tmax:
                pointers_to_trace_optimal_alignment[i + 1, j + 1] += 3
            if temporary_scores[2] == tmax:
                pointers_to_trace_optimal_alignment[i + 1, j + 1] += 4

    inverted_x_result, inverted_y_result = trace_through_optimal_alignment(pointers_to_trace_optimal_alignment,
                                                                           sequence_one,
                                                                           sequence_two)

    return '\n'.join([inverted_x_result, inverted_y_result])


def trace_through_optimal_alignment(pointers_to_trace_optimal_alignment: np.ndarray,
                                    sequence_one: str,
                                    sequence_two: str) -> tuple[str, str]:
    """
    Builds optimal alignment based on the scores matrix
    :param pointers_to_trace_optimal_alignment: optimal alignment scores
    :param sequence_one: first sequence (x dimension of the matrix)
    :param sequence_two: second sequence (y dimension of the matrix)
    :return: two strings representing optimal alignment
    """
    i = len(sequence_one)
    j = len(sequence_two)
    result_x_dimension = []
    result_y_dimension = []
    while i > 0 or j > 0:
        if pointers_to_trace_optimal_alignment[i, j] in [2, 5, 6, 9]:
            result_x_dimension.append(sequence_one[i - 1])
            result_y_dimension.append(sequence_two[j - 1])
            i -= 1
            j -= 1
        elif pointers_to_trace_optimal_alignment[i, j] in [3, 5, 7, 9]:
            result_x_dimension.append(sequence_one[i - 1])
            result_y_dimension.append('-')
            i -= 1
        elif pointers_to_trace_optimal_alignment[i, j] in [4, 6, 7, 9]:
            result_x_dimension.append('-')
            result_y_dimension.append(sequence_two[j - 1])
            j -= 1
    # Reverse the strings.
    inverted_x_result = ''.join(result_x_dimension)[::-1]  # todo: extract method, apply to each
    inverted_y_result = ''.join(result_y_dimension)[::-1]
    return inverted_x_result, inverted_y_result


def initialise_grid(gap: int, grid_x_dimension: int, grid_y_dimension: int) -> np.ndarray:
    """
    Initialise scores matrix based on the given dimensions
    :param gap: cost of the gap
    :param grid_x_dimension: x dimension of the grid
    :param grid_y_dimension: y dimension of the grid
    :return: initialised grid
    """
    scores_grid = np.zeros((grid_x_dimension + 1, grid_y_dimension + 1))
    scores_grid[:, 0] = np.linspace(0, -grid_x_dimension * gap, grid_x_dimension + 1)
    scores_grid[0, :] = np.linspace(0, -grid_y_dimension * gap, grid_y_dimension + 1)
    return scores_grid

#todo: create test out of the examples
x = "GATTACA"
y = "GCATGCU"
print(needleman_wunsch(x, y))
