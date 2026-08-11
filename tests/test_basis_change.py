"""
Test script for the basis transformation matrix.
For all non-zero Miller indices (h,k,l) within the range [-n, n],
verify that the matrix M = transpose(inv(get_new_basis(h,k,l)))
- is integer-valued,
- has determinant ±1,
- transforms the reduced (h,k,l) vector into (0,0,±1).
"""

import math
import numpy as np
from layer_shifter.math_utils import get_new_basis


def test_basis_matrix_all_indices(n: int = 20) -> None:
    """
    Loop over all hkl in the cube [-n, n]³ (excluding the origin).
    For each triplet, compute the basis-change matrix and check its properties.

    Parameters
    ----------
    n : int
        Half‑side of the index cube to test (default 3).
    """
    for h_raw in range(-n, n + 1):
        for k_raw in range(-n, n + 1):
            for l_raw in range(-n, n + 1):
                if h_raw == 0 and k_raw == 0 and l_raw == 0:
                    continue

                # Reduce indices by their greatest common divisor
                gcd = math.gcd(math.gcd(h_raw, k_raw), l_raw)
                h, k, l = h_raw // gcd, k_raw // gcd, l_raw // gcd

                # Compute the transformation matrix used in change_basis()
                M_float = get_new_basis(h, k, l)

                # ---- Check 1: matrix elements are integers (up to rounding) ----
                assert np.allclose(M_float, np.round(M_float)), (
                    f"Matrix not integer for ({h_raw},{k_raw},{l_raw})"
                )
                M = np.round(M_float).astype(int)

                # ---- Check 2: determinant is ±1 ----
                det = int(round(np.linalg.det(M)))
                assert abs(det) == 1, (
                    f"Determinant is {det} for ({h_raw},{k_raw},{l_raw}), expected ±1"
                )

                # ---- Check 3: (h,k,l) maps to (0,0,±1) ----
                prod = M @ np.array([h, k, l])
                expected = np.array([0, 0, 1]) if prod[2] > 0 else np.array([0, 0, -1])
                assert np.array_equal(prod, expected), (
                    f"Mapping failed for ({h_raw},{k_raw},{l_raw}): "
                    f"got {prod}, expected {expected}"
                )

    print(f"All indices in [-{n}, {n}]³ passed.")

test_basis_matrix_all_indices()