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

