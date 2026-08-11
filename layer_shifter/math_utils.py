import numpy as np
from typing import List, Tuple, Optional, Set


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean algorithm: returns (gcd, x, y) such that a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x


def solve_diophantine(a: int, b: int, c: int) -> Optional[Tuple[int, int]]:
    """Solve the linear Diophantine equation a*y + b*z = c.
    Returns (y, z) or None if no solution exists."""
    if a == 0 and b == 0:
        return (0, 0) if c == 0 else None

    g, x0, y0 = extended_gcd(a, b)

    if g == 0:
        return (0, 0) if c == 0 else None

    if c % g != 0:
        return None

    factor = c // g
    y = x0 * factor
    z = y0 * factor
    return y, z


def mathematics_rounding(number: float) -> int:
    """Round according to standard arithmetic rules."""
    if number > 0:
        return int(number + 0.5)
    else:
        return int(number + -0.5)


def find_vars(h: int, k: int, l: int,
              fixed_var: int = 0,
              fixed_value: int = 1) -> Optional[List[int]]:
    """Find integer solutions to hx + ky + lz = 1 with one variable fixed.
    Returns [x, y, z] or None."""
    if fixed_var == 0:
        c = 1 - h * fixed_value
        a, b = k, l
        solution = solve_diophantine(a, b, c)
        if solution is None:
            return None
        y, z = solution
        return [fixed_value, y, z]
    elif fixed_var == 1:
        c = 1 - k * fixed_value
        a, b = h, l
        solution = solve_diophantine(a, b, c)
        if solution is None:
            return None
        x, z = solution
        return [x, fixed_value, z]
    elif fixed_var == 2:
        c = 1 - l * fixed_value
        a, b = h, k
        solution = solve_diophantine(a, b, c)
        if solution is None:
            return None
        x, y = solution
        return [x, y, fixed_value]
    else:
        raise ValueError()


def get_new_basis(h: int, k: int, l: int) -> np.ndarray:
    """
    Return an integer unimodular matrix M (to be used as a supercell
    transformation) such that the (hkl) plane of the original lattice
    becomes the (001) plane of the new lattice.

    The first two rows of M are [uvw] vectors chosen to lie in the (hkl) plane; this
    automatically makes the third row point along the plane normal (the
    desired new c‑axis).  The algorithm searches among several simple
    Diophantine solutions and picks the one with the smallest absolute
    vector components for numerical convenience.
    """
    vars_list = [find_vars(h, k, l, 0, 1), find_vars(h, k, l, 1, 1), find_vars(h, k, l, 2, 1),
                 find_vars(h, k, l, 0, -1), find_vars(h, k, l, 1, -1), find_vars(h, k, l, 2, -1)]
    fixed_var_list = ["x", "y", "z", "-x", "-y", "-z"]
    abs_var_list = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        if vars_list[i] is not None:
            abs_var_list[i] = 1 / sum([abs(value) for value in vars_list[i]])

    fixed_var = fixed_var_list[abs_var_list.index(max(abs_var_list))]
    x, y, z = vars_list[abs_var_list.index(max(abs_var_list))]
    # print(fixed_var)
    matrix = np.zeros((3, 3))
    if fixed_var == "x":
        matrix = np.array([[-y, 1, 0], [-z, 0, 1], [h, k, l]])
    elif fixed_var == "y":
        matrix = np.array([[-1, x, 0], [0, -z, 1], [h, k, l]])
    elif fixed_var == "z":
        matrix = np.array([[1, 0, -x], [0, 1, -y], [h, k, l]])

    if fixed_var == "-x":
        matrix = np.array([[-y, -1, 0], [z, 0, 1], [h, k, l]])
    elif fixed_var == "-y":
        matrix = np.array([[1, x, 0], [0, z, 1], [h, k, l]])
    elif fixed_var == "-z":
        matrix = np.array([[-1, 0, -x], [0, 1, y], [h, k, l]])
    final_matrix = np.transpose(np.linalg.inv(matrix))
    return final_matrix
