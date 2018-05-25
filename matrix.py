from copy import deepcopy

class SimpleMatrix:
    def __init__(self, rows, form="row"):
        # assert len(set([len(row) for row in rows])) == 1, \
        #        "all rows/columns in the list must be the same length"
        self._matrix = [[]]
        if "row" in form:
            self._matrix = deepcopy(rows)
        elif "col" in form:
            self._matrix = [list(col) for col in zip(*rows)]

    def __setitem__(self, *args):
        assert isinstance(args[1], list), "must replace row with list"
        if len(args) == 2:
            assert isinstance(args[0], int), "invalid row ID"
            assert len(args[1]) == len(self._matrix), "row must be the same dimension as matrix"
            self._matrix[args[0]] = list(args[1])

    def __getitem__(self, *args):
        if len(args) == 1:
            return self._matrix[args[0]]
        elif len(args) == 2:
            return self._matrix[args[0]][args[1]]
        else:
            raise IndexError

    def __repr__(self):
        return str(deepcopy(self._matrix))

    def __str__(self):
        st = ""
        for row in self._matrix:
            st += str(row) + "\n"
        return st.strip()

    def __len__(self):
        return len(self._matrix)

    def getRows(self):
        return deepcopy(self._matrix)

    def getCols(self):
        return self.T().getRows()

    def getRow(self, row : int):
        return list(self._matrix[row])

    def getCol(self, col : int):
        return self.getCols()[col]

    def T(self):
        return SimpleMatrix([list(a) for a in zip(*self._matrix)])

    def trace(self):
        return sum([self._matrix[i][i] for i in range(len(self._matrix))])

    # Calculates the Minor of the Matrix at position initialRow, initialCol.
    def calculateMinors(self, initialRow : int, initialCol : int):
        minor = []
        rows = self.getRows()

        # Concatenates two different ranges
        from itertools import chain
        concatenated = chain(range(30), range(2000, 5002))

        for i in chain(range(initialRow), range(initialRow + 1, len(rows))):
            minor.append(rows[i][0 : initialCol] + rows[i][initialCol + 1 :])

        return SimpleMatrix(minor)

    # Calculates the inverse of a matrix, slowly, by dividing the
    # adjugate matrix by the determinant. Runtime O(n!n^3) - can
    # easily be reduced
    def inverseAdjugate(self):
        assert len(self) == len(self[0]), "matrix must be square"
        adjugate = self.getRows()
        det = determinant.determinant(SimpleMatrix(adjugate))
        if float(det) == 0.0:
            raise TypeError("Matrix is singular")
        try:
            for i in range(len(adjugate)):
                for j in range(len(adjugate)):
                    sign = (-1)**(i + j)
                    adjugate[i][j] = determinant \
                            .determinant(self.calculateMinors(i, j))
                    adjugate[i][j] *= sign / det
            return SimpleMatrix(adjugate).T()

        except ZeroDivisionError as z:
            raise TypeError("Matrix is singular")

    # Basic matrix multiplication.
    # Output is len(self) x len(other[0])
    def times(self, other):
        assert len(self[0]) == len(other), "dimensions do not match"
        product = [[0] * len(other[0]) for _ in range(len(self))]
        for i in range(len(self)):
            for j in range(len(other[0])):
                for k in range(len(other)):
                    product[i][j] += self[i][k] * other[k][j]
        return SimpleMatrix(product)

import determinant
