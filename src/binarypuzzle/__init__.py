# Copyright (c) 2020 Alexander Færøy. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import annotations

from .constants import N
from .exceptions import InvalidPuzzleError, UnsolvablePuzzleError

from functools import reduce
from typing import List, Optional, Tuple
from z3 import sat, And, Int, Not, Or, Solver, Sum


__all__ = ["BinaryPuzzle", "InvalidPuzzleError", "N", "UnsolvablePuzzleError"]


class BinaryPuzzle:
    def __init__(self, puzzle: List[List[Optional[int]]]) -> None:
        """ Create a new BinaryPuzzle instance.

        >>> puzzle = BinaryPuzzle([
        ...     [N, 1],
        ...     [N, N],
        ... ])
        """

        size = len(puzzle)

        # Ensure that our given puzzle is NOT empty.
        if size == 0:
            raise InvalidPuzzleError

        # Ensure that our given puzzle is N x N.
        if reduce(lambda acc, row: acc + len(row), puzzle, 0) != size ** 2:
            raise InvalidPuzzleError

        # Ensure that our N is even.
        if size % 2 != 0:
            raise InvalidPuzzleError

        # Check that all values are either 0, 1, or None.
        for row in puzzle:
            for value in row:
                if value not in {0, 1, None}:
                    raise InvalidPuzzleError

        # Our input puzzle is good.
        self._puzzle = puzzle
        self._size = size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BinaryPuzzle):
            return NotImplemented

        return self.rows() == other.rows()

    def rows(self) -> List[List[Optional[int]]]:
        result = []

        for row in self._puzzle:
            result.append(row)

        return result

    def columns(self) -> List[List[Optional[int]]]:
        result = []
        size = self.size()

        for y in range(size):
            column = []

            for x in range(size):
                column.append(self._puzzle[x][y])

            result.append(column)

        return result

    def size(self) -> int:
        """ Returns the size of the given puzzle.

        >>> puzzle = BinaryPuzzle([
        ...     [N, 1],
        ...     [N, N],
        ... ])

        >>> puzzle.size()
        2
        """

        return self._size

    def positions(self) -> List[Tuple[int, int]]:
        """ Returns the size of the given puzzle.

        >>> puzzle = BinaryPuzzle([
        ...     [N, 1],
        ...     [N, N],
        ... ])

        >>> puzzle.size()
        2

        >>> puzzle.positions()
        [(0, 0), (0, 1), (1, 0), (1, 1)]
        """

        size = self.size()
        return [(x, y) for x in range(size) for y in range(size)]

    def solve(self) -> BinaryPuzzle:
        # Constants.
        size = self.size()

        # Our z3 Solver.
        solver = Solver()

        # Our mapping between an (x, y) position in our puzzle and the symbolic
        # variable that z3 is going to use to represent the integer value in
        # our matrix.
        symbols = {(x, y): Int("({}, {})".format(x, y)) for x, y in self.positions()}

        # We will often have to work with either rows of symbolic variables or
        # columns of symbolic variables. We start with rows:
        rows = []

        for x in range(size):
            row = [symbols[(x, y)] for y in range(size)]
            rows.append(row)

        # We define a list of columns:
        columns = []

        for y in range(size):
            column = [symbols[(x, y)] for x in range(size)]
            columns.append(column)

        # We start by adding the values from our puzzle to the solver.
        for x, y in self.positions():
            value = self._puzzle[x][y]

            # We skip our None values since they are the values we are
            # interested in finding.
            if value is None:
                continue

            # This would be equivalent to assigning a value to a variable in
            # the non-symbolic world.
            solver.add(symbols[(x, y)] == value)

        # We can now begin to add constraints to our model. The first and most
        # simple constraint we add is that each cell must either contain a 0 or
        # a 1 value. No other values are interesting if we are searching for
        # the result.
        for symbol in symbols.values():
            solver.add(Or([symbol == value for value in [0, 1]]))

        # The second constraint we add, is to ensure that each row have the
        # exact same amount of zeroes and ones. We can exploit the nature of
        # our matrix here because we know that each row and column contain an
        # even amount of items. This allows us to simply check if half of the
        # elements are zeros (and thus we imply that the other half of the
        # elements contains ones). This simplifies the problem into simply
        # being that the sum of each element in a row must be half the size of
        # our row:
        for row in rows:
            solver.add(Sum(row) == size // 2)

        # We do the same trick for our columns:
        for column in columns:
            solver.add(Sum(column) == size // 2)

        # We need to add a constraint to make sure that each of our rows and
        # columns are unique. There must be a smarter way to do this.
        # We start with the rows:
        solver.add(
            Not(
                Or(
                    [
                        And([a == b for a, b in zip(row_a, row_b)])
                        for row_a in rows
                        for row_b in rows
                        if row_a != row_b
                    ]
                )
            )
        )

        # We repeat the same for columns:
        solver.add(
            Not(
                Or(
                    [
                        And([a == b for a, b in zip(column_a, column_b)])
                        for column_a in columns
                        for column_b in columns
                        if column_a != column_b
                    ]
                )
            )
        )

        # The last constraint we need to add only applies for puzzles that are
        # larger than 2x2:
        if size > 2:
            # We need to check that in each row and each column that no more
            # than two of the same numbers are next or below each other. We can
            # build an overlapping window of each triplet in a given row or
            # column to simplify this.
            #
            # This gives us the following possible values of our triplets:
            #
            #   (0, 0, 0) => Illegal.
            #   (0, 0, 1) => Legal.
            #   (0, 1, 0) => Legal.
            #   (0, 1, 1) => Legal.
            #   (1, 0, 0) => Legal.
            #   (1, 0, 1) => Legal.
            #   (1, 1, 0) => Legal.
            #   (1, 1, 1) => Illegal.
            #
            # My first intuition here solved this issue as following: we can
            # now identify that we cannot allow an overlapping window where the
            # sum of the 3 elements in the window is either 0 or 3:
            #
            # But a much simpler method is that given each triplet (a, b, c) to
            # check that none of the them satisfies And([a == b, b == c]).
            #
            # We can model this easily in z3. We start with the rows:
            for row in rows:
                # We create our overlapping windows.
                for i in range(size - 2):
                    i_end = i + 3
                    a, b, c = row[i:i_end]
                    solver.add(Not(And([a == b, b == c])))

            # We do the same thing to our columns:
            for column in columns:
                # We create our overlapping windows.
                for i in range(size - 2):
                    i_end = i + 3
                    a, b, c = column[i:i_end]
                    solver.add(Not(And([a == b, b == c])))

        # Check if our solver can find a solution.
        if solver.check() != sat:
            raise UnsolvablePuzzleError

        # Our model.
        model = solver.model()

        # Evaluate our model and print the resulting grid.
        result = {
            position: model.evaluate(symbol) for position, symbol in symbols.items()
        }

        # Return our result in the same format as our input.
        return BinaryPuzzle(
            [[result[(x, y)].as_long() for y in range(size)] for x in range(size)]
        )
