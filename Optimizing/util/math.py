# Library-like script providing mathematical utility functions.

import datetime
import operator as op
from functools import reduce
from numpy import array, diag, zeros
from scipy.linalg import svd as scipy_svd



# Handy function to easily process missing values
# Params: Any
# Return: Any
def none_2_zero(value):
    return 0 if value is None else value


# Handy function to calculate average of list of values (can handle empty list)
# Params: list<float>, [list<float>]
# Return: float
def average(values, weights=None):
    if len(values) == 0:
        return 0

    if weights is None:
        weights = [1] * len(values)

    if len(values) != len(weights):
        raise ValueError('Values and weights do not have the same length')

    return reduce(op.add, [value * weight for value, weight in zip(values, weights)]) / len(values)


# Performs SVD on a maxtrix - reduces number of columns to desired amount with preserving structural relationships.
# Source: https://machinelearningmastery.com/singular-value-decomposition-for-machine-learning/
# Params: list<list<float>>, int, [int]
# Return: list<list<float>>
def svd(matrix, n_elements, ndigits=2):
    A = array(matrix)
    # Singular-value decomposition
    U, s, _ = scipy_svd(A)
    # create m x n Sigma matrix
    Sigma = zeros((A.shape[0], A.shape[1]))
    # populate Sigma with n x n diagonal matrix
    Sigma[:A.shape[0], :A.shape[0]] = diag(s)
    # select
    Sigma = Sigma[:, :n_elements]
    # transform
    T = U.dot(Sigma)
    T = T.tolist()

    new_matrix = {}
    for word, vector in zip(matrix, T):
        new_matrix[word] = [round(x, ndigits=ndigits) for x in vector]

    return new_matrix

def svd_part_1(matrix):
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}]     Part 1: Step 1/4')
    A = array([matrix[key] for key in matrix])

    # Singular-value decomposition
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}]     Part 1: Step 2/4')
    U, s, _ = scipy_svd(A)

    # create m x n Sigma matrix
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}]     Part 1: Step 3/4')
    Sigma = zeros((A.shape[0], A.shape[1]))

    # populate Sigma with n x n diagonal matrix
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}]     Part 1: Step 4/4')
    Sigma[:A.shape[0], :A.shape[0]] = diag(s)

    return {'sigma': Sigma, 'u': U}


def svd_part_2(part1_products, n_elements):
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}]     Part 2: Step 1/3')
    Sigma = part1_products['sigma'][:, :n_elements]

    # transform
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}]     Part 2: Step 2/3')
    T = part1_products['u'].dot(Sigma)

    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}]     Part 2: Step 3/3')
    T = T.tolist()

    return T