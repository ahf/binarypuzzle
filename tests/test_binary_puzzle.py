# Copyright (c) 2020 Alexander Færøy. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from binarypuzzle import BinaryPuzzle, N, InvalidPuzzleError, UnsolvablePuzzleError


class BinaryPuzzleTest(unittest.TestCase):
    def test_simple_2x2(self) -> None:
        puzzle = BinaryPuzzle([
            [0, 1],
            [1, 0],
        ])

        self.assertEqual(puzzle.size(), 2)
        self.assertEqual(puzzle.positions(), [(0, 0), (0, 1),
                                              (1, 0), (1, 1)])
        self.assertEqual(puzzle.rows(), [
            [0, 1],
            [1, 0]
        ])

        self.assertEqual(puzzle.columns(), [
            [0, 1],
            [1, 0],
        ])

        # This puzzle is already solved.
        solved_puzzle = puzzle.solve()
        self.assertEqual(puzzle, solved_puzzle)

    def test_simple_4x4(self) -> None:
        puzzle = BinaryPuzzle([
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [0, 1, 0, 1],
            [1, 0, 1, 0],
        ])

        self.assertEqual(puzzle.size(), 4)
        self.assertEqual(puzzle.positions(), [(0, 0), (0, 1), (0, 2), (0, 3),
                                              (1, 0), (1, 1), (1, 2), (1, 3),
                                              (2, 0), (2, 1), (2, 2), (2, 3),
                                              (3, 0), (3, 1), (3, 2), (3, 3)])

        self.assertEqual(puzzle.rows(), [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [0, 1, 0, 1],
            [1, 0, 1, 0],
        ])

        self.assertEqual(puzzle.columns(), [
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
        ])

        # This puzzle is already solved.
        solved_puzzle = puzzle.solve()
        self.assertEqual(puzzle, solved_puzzle)

    def test_invalid(self) -> None:
        # Empty puzzles are invalid.
        with self.assertRaises(InvalidPuzzleError):
            BinaryPuzzle([])

        # Invalid dimensions.
        with self.assertRaises(InvalidPuzzleError):
            BinaryPuzzle([
                [0, 1],
                [0],
            ])

        # The number if rows and columns must be an even number.
        with self.assertRaises(InvalidPuzzleError):
            BinaryPuzzle([
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ])

        # Only 0, 1, and None are valid values.
        with self.assertRaises(InvalidPuzzleError):
            BinaryPuzzle([
                [1, 2],
                [3, 4],
            ])

        # The road to 100% coverage is hard, but somebody have
        # to do it.
        self.assertFalse(BinaryPuzzle([[0, 1], [1, 0]]) == 42)

    def test_unsolvable(self) -> None:
        with self.assertRaises(UnsolvablePuzzleError):
            puzzle = BinaryPuzzle([
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ])

            puzzle.solve()

        with self.assertRaises(UnsolvablePuzzleError):
            puzzle = BinaryPuzzle([
                [1, 1],
                [1, N],
            ])

            puzzle.solve()

    def test_simple_solve(self) -> None:
        puzzle = BinaryPuzzle([
            [1, N, N, 0, N, N],
            [N, N, 0, 0, N, 1],
            [N, 0, 0, N, N, 1],
            [N, N, N, N, N, N],
            [0, 0, N, 1, N, N],
            [N, 1, N, N, 0, 0],
        ])

        result = puzzle.solve()

        self.assertEqual(result.rows(), [
            [1, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 1, 1],
            [1, 0, 0, 1, 0, 1],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 0, 0],
        ])

    def test_hard_solve(self) -> None:
        puzzle = BinaryPuzzle([
            [N, N, N, N, 1, 0, N, N, N, N, N, N, N, 1],
            [1, N, N, N, N, 0, N, N, N, 1, N, 1, N, 1],
            [N, N, 1, N, N, N, 1, N, N, N, N, N, N, N],
            [0, N, N, N, N, 1, 1, N, N, N, N, 0, N, 1],
            [0, N, 0, N, N, N, N, N, 1, N, N, N, N, 1],
            [N, 0, N, N, N, N, N, N, 0, N, N, N, N, N],
            [N, N, 1, N, N, N, N, N, N, 1, N, N, 1, N],
            [N, N, 1, N, 0, N, N, 1, N, N, 0, N, N, N],
            [N, N, N, N, N, 1, N, 1, N, N, N, N, 1, N],
            [0, N, 1, 0, N, 1, N, N, N, N, 0, N, N, N],
            [N, N, 1, N, N, N, N, N, N, N, 0, 0, N, N],
            [N, N, N, 0, N, N, N, N, N, N, N, N, N, N],
            [N, 1, N, N, N, N, N, N, N, 0, N, N, N, N],
            [N, N, 0, N, N, N, 0, N, N, N, N, 0, N, N],
        ])

        result = puzzle.solve()

        self.assertEqual(result.rows(), [
            [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1],
            [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0],
            [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
        ])

        # Check that our result have the same size as our input.
        self.assertEqual(puzzle.size(), result.size())

        # Check that our solver didn't change any of the non-None input values.
        input_puzzle = puzzle.rows()
        result_puzzle = result.rows()

        for x, y in puzzle.positions():
            input_value = input_puzzle[x][y]
            result_value = result_puzzle[x][y]

            if input_value is N:
                continue

            self.assertEqual(input_value, result_value)

        # Make sure we have the right number of N's, zeros, and ones in each
        # row and column.
        for values in result.rows() + result.columns():
            self.assertEqual(values.count(N), 0)
            self.assertEqual(values.count(0), 7)
            self.assertEqual(values.count(1), 7)

        # Make sure that each row and each column is unique. Lists in
        # Python are not hashable, so we convert each row and each column
        # to a tuple to store them in a set.
        unique_rows = set(list(map(lambda x: tuple(x), result.rows())))
        self.assertEqual(len(unique_rows), 14)

        unique_columns = set(list(map(lambda x: tuple(x), result.columns())))
        self.assertEqual(len(unique_columns), 14)

        # Sanity check that our rows and column aren't the same in case
        # we messed up the rows() and columns()
        # implementations.
        self.assertNotEqual(unique_rows, unique_columns)

        # Check if we have any [0, 0, 0] or [1, 1, 1] sublists in our
        # rows and columns:
        for value in result.rows() + result.columns():
            value_len = len(value)
            self.assertEqual(value_len, 14)

            for i in range(value_len):
                self.assertNotEqual([0, 0, 0], value[i:i + 3])
                self.assertNotEqual([1, 1, 1], value[i:i + 3])
