from copy import deepcopy
import fractions
# Canonical basis for Pn(R) = {1, x, ..., x^n}
# Factors polynomials using the rational root theorem.

# This function converts any polynomial in string form
# into a list consisting of the individual terms.
def convertPolynomial(s : str, var="x"):
    # This function combines like terms in the polynomial.
    def combineLikeTerms():
        nonlocal returnForm
        constants, seen = [], []
        # Creates a list of dictionaries corresponding with
        # whether the term's vector already exists in the
        # string; if so, then add the coefficients, and if
        # not, then add it to the list and continue.
        for i in range(len(returnForm)):
            if returnForm[i]:
                if var not in returnForm[i]:
                    constants.append(int(returnForm[i]))
                else:
                    vector = returnForm[i][returnForm[i].index(var):]
                    coeff = returnForm[i][:returnForm[i].index(var)]
                    possible = list(filter(lambda x : x.get(vector, -1) \
                            != -1, seen))
                    if possible == []:
                        seen.append({vector : [int(coeff)]})
                    else:
                        seen[seen.index(possible[0])][vector] \
                                .append(int(coeff))
        # The following line takes the list of dictionaries, sums
        # the values of the coefficients, and prepends it to the
        # key of the dictionary, which contains the common vector.
        # Then, it adds the constant terms to the list as well.
        # Terms like '0x^2' and '0' are valid, and are removed in
        # the return statement.
        combinedNoZero = [str(sum(d[list(d.keys())[0]])) + \
                list(d.keys())[0] for d in seen] + \
                [str(sum(constants))]
        return [val for val in combinedNoZero \
                if (var in val and int(val[:val.index(var)]) != 0) \
                or (var not in val and int(val) != 0)]
    listForm = "+-".join("".join(s.split()).split('-')).split('+')
    returnForm = []
    # Creates a list containing the individual terms, and prepends
    # the vectors 'without coefficient' with the value 1, to be used
    # in further processing.
    for val in listForm:
        try:
            if val.index(var) - 1 < 0:
                raise ValueError
            int(val[val.index(var) - 1])
            returnForm.append(val)
        except ValueError:
            if var not in val:
                returnForm.append(val)
            else:
                returnForm.append("1{}".join(val.split(var)).format(var))
    returnForm = combineLikeTerms()
    return Matrix([[var] for var in sorted(returnForm, \
        key=make_comparator(var), reverse=True)])

# Source: http://code.activestate.com/recipes/576653-convert-a-cmp-function-to-a-key-function/
# Comparator that orders the elements of the basis
# in the order of the canonical basis of Pn(R).
def make_comparator(var : str):
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return compare(self.obj, other.obj) < 0
        def __gt__(self, other):
            return compare(self.obj, other.obj) > 0
        def __eq__(self, other):
            return compare(self.obj, other.obj) == 0
        def __le__(self, other):
            return compare(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return compare(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return compare(self.obj, other.obj) != 0

    def compare(x, y):
        if var not in x and var not in y:
            if int(x) > int(y):
                return -1
            else:
                return 1
        if var in x and var not in y:
            return -1
        if var in y and var not in x:
            return 1
        if var in x and var in y:
            if '^' not in x and '^' in y:
                return 1
            elif '^' in x and '^' not in y:
                return -1
            else:
                x_val = str(x[x.index('^') + 1:])
                y_val = str(y[y.index('^') + 1:])
                return compare(x_val, y_val)
    return K

# Creates a basis for any given polynomial, and returns
# it, as well as the guise of the vector with respect to
# the basis.
def makeBasisForVector(s, var="x"):
    vector, basis = [], []
    if not isinstance(s, Matrix):
        reduced = convertPolynomial(s, var)
    else:
        reduced = s
    for vect in reduced:
        vec = vect[0]
        if var not in vec:
            vector.append(vec)
        else:
            vector.append(vec[:vec.index(var)])
    for vect in reduced:
        vec = vect[0]
        if var not in vec:
            basis.append(1)
        else:
            basis.append(vec[vec.index(var):])
    return Matrix([[lst] for lst in basis]), \
            Matrix([[lst] for lst in vector])

def basisStandard(terms: tuple, var="x"):
    basis = terms[0]
    values = terms[1]
    if basis[-1] == 1:
        pass

# Rewrites the basis in terms of the standard quadratic.
def basisStandardQuadratic(terms: tuple, var="x"):
    basis = terms[0]
    values = terms[1]
    assert len(basis) <= 3, "highest power must be less than 2"
    if not basis[-1]:
        return
    elif basis[-1][0] == 1:
        return Matrix([[1], ['x'], ['x^2']]), \
                Matrix([values[-1], ['0'], ['0']])
    else:
        largestPower = basis[-1][0][basis[-1][0].index(var) + 1:]
        return largestPower

def quadraticFormula(matrix, var="x"):
    # Formula:
    if not isinstance(matrix, Matrix):
        terms = basisStandardQuadratic(makeBasisForVector(matrix), var)
    else:
        terms = basisStandardQuadratic(matrix)
    return terms

def characteristicPolynomial(matrix, var="x"):
    if len(matrix) == 2:
        return 4

import matrix
