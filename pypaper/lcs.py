#!/usr/bin/env python
# -*- coding: utf-8 -*-


def lcs(a, b):
    return levenshtein(
        a,
        b,
        insertion_cost=1,
        first_insertion_cost=50,
        prepend_first_insertion_cost=10,
        append_first_insertion_cost=5,
        deletion_cost=100,
        substitution_cost=100,
        transposition_cost=10,
        memo=[],
        precol=[]
    )


def levenshtein(
    s1,
    s2,
    deletion_cost=1,
    insertion_cost=1,
    first_insertion_cost=1,
    prepend_first_insertion_cost=1,
    append_first_insertion_cost=1,
    substitution_cost=1,
    transposition_cost=1,
    memo=[],
    precol=[]
):
    previous_row = 0
    last_is_insertion = 1

    if not precol:
        a = [0 for i in range(2)]
        a[last_is_insertion] = float('inf')
        precol = [a] * (len(s1) + 1)
    else:
        assert len(precol) == len(s1) + 1

    if not memo:
        row = [[0, 0] for i in range(len(s2) + 1)]
        row[0][last_is_insertion] = precol[0][last_is_insertion]
        row[0][1 - last_is_insertion] = precol[0][1 - last_is_insertion]
        for i in range(1, len(s2) + 1):
            row[i][last_is_insertion] = min(
                row[0][last_is_insertion],
                row[0][1 - last_is_insertion] + (prepend_first_insertion_cost - insertion_cost)
            ) + i * insertion_cost
            row[i][1 - last_is_insertion] = float('inf')
        memo.append(row)

    for i, c1 in list(enumerate(s1))[len(memo) - 1:]:
        previous_row = i
        current_row = i + 1
        memo.append([[0, 0] for i in range(len(s2) + 1)])
        memo[current_row][0][1 - last_is_insertion] = (
            min(precol[current_row])
            + (i + 1) * deletion_cost
        )
        # append is not insertion
        actual_first_insertion_cost = (
            append_first_insertion_cost if i == len(s1) - 1
            else first_insertion_cost
        )
        memo[current_row][0][last_is_insertion] = float('inf')
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer
            insertions = min(
                memo[current_row][j][last_is_insertion] + insertion_cost,
                memo[current_row][j][1 - last_is_insertion] + actual_first_insertion_cost
            )
            deletions = min(memo[previous_row][j + 1]) + deletion_cost
            substitutions = min(memo[previous_row][j]) + (c1 != c2) * substitution_cost
            memo[current_row][j + 1][last_is_insertion] = insertions
            memo[current_row][j + 1][1 - last_is_insertion] = min(deletions, substitutions)

    return min(memo[len(s1)][-1])
