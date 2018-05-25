from copy import deepcopy

# Calculates in O(n^3) time the determinant of a matrix,
# by converting it to upper triangular, and multiplying
# along the diagonal of the matrix.
def determinant(matrix):
    assert(len(matrix[0]) == len(matrix)), "must be square"
    return quickDeterminant(matrix)

# Converts a matrix into upper triangular form, so that
# its determinant can be easily computed by multiplying
# every element of the diagonal.
def quickDeterminant(matrix):
    if len(matrix) == 0:
        return
    elif len(matrix) == 1:
        if isinstance(matrix[0], int):
            return matrix[0]
        elif len(matrix[0]) == 0:
            return
        else:
            return matrix[0][0]

    matrix, sign = convertToUpperTriangular(matrix)
    if matrix == -1:
        return 0
    product = 1
    for i in range(len(matrix)):
        product *= matrix[i][i]
    return sign * product

# Converts a matrix into its upper triangular form. The algorithm
# used for this is simple. First, find the row which contains a
# non-zero element in the first column, and swap this with the
# first row; if none exists, the determinant is zero. Then, use
# type three row operations (see Friedberg's Linear Algebra) to
# change the all the elements of the first column besides the first
# to zero. Then, ignore the first row and first column, and repeat.
def convertToUpperTriangular(matrix ):
    # Switches the rows of a matrix by their index.
    def switchRow(matrix, row : int, replacement : int):
        if row == replacement:
            return matrix
        else:
            nonlocal sign
            temp = matrix[row]
            matrix[row] = matrix[replacement]
            matrix[replacement] = temp
            sign *= -1
            return matrix

    # The sign is important, because if B is matrix identical to A
    # except for two swapped rows, then det(B) = -det(A). This can
    # be proven by looking at how the determinant arises from the
    # wedge product of a vector space V with itself, dim(V) times.
    sign = 1
    currCol = 0
    firstRow = 0
    matrix = deepcopy(matrix) # Done to avoid destroying the original
    while currCol < len(matrix) - 1:
        minor = Matrix(generateSmaller(matrix, firstRow, currCol))
        firstNonZero = checkColumn(minor, 0) # Checks for first nonzero row
        if firstNonZero == -1:
            return -1
        else:
            switchRow(matrix, firstRow, firstNonZero + firstRow)
            # Does type three row operations by finding the ratio needed
            # to add the "first" row to the current row to obtain zero.
            # Then, add the two rows together.
            for row in range(firstRow + 1, len(matrix)):
                if matrix[row][currCol] == 0:
                    continue
                ratio = matrix[row][currCol] / matrix[firstRow][currCol]
                tempRow = [x * -ratio for x in matrix[firstRow]]
                newRow = [x + y for x, y in zip(matrix[row], tempRow)]
                matrix[row] = newRow
            currCol += 1
            firstRow += 1
    return matrix, sign

# Returns the index of the first nonzero element.
def checkColumn(matrix, column : int):
    return next((i for i, \
            x in enumerate(matrix.getCol(column)) if x), -1)

# This generates the matrix whose 0, 0 coordinate is the same as
# the initialRow, initialCol coordinate in the original matrix.
# This will be used to calculate the first nonzero element, used to
# to calculate the determinant of the main matrix. This is also
# equivalent to the matrix minor at 0, 0.
def generateSmaller(matrix , initialRow : int, initialCol : int):
    rows = matrix.getRows()
    rows = rows[initialRow:]
    for i in range(len(rows)):
        rows[i] = rows[i][initialCol:]
    return rows

# Calculates the determinant of a matrix recursively from the top row
# of the matrix's cofactor. See "cofactor expansion".
# This has a runtime of O(k!)
def slowDeterminant(matrix):
    assert(len(matrix[0]) == len(matrix)), "must be square"
    if len(matrix) == 0:
        return
    elif len(matrix) == 1:
        if isinstance(matrix[0], int):
            return matrix[0]
        elif len(matrix[0]) == 0:
            return
        else:
            return matrix[0][0]
    # ad - bc
    elif len(matrix) == 2:
        return matrix[1][1] * matrix[0][0] - matrix[0][1] \
                * matrix[1][0]
    else:
        total = 0
        for i in range(len(matrix[0])):
            sign = 1 if i % 2 == 0 else -1
            test = sign * matrix[0][i] \
                    * slowDeterminant(matrix.calculateMinors(0, i))
            total += test
    return total

from matrix import SimpleMatrix as Matrix
