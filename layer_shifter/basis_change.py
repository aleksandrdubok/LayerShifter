import math
from typing import List, Tuple
from pymatgen.core import Structure
from layer_shifter.io import write_structure

from layer_shifter.io import save_basis_matrix
from layer_shifter.math_utils import get_new_basis



import logging
logger = logging.getLogger(__name__)

# basis change part
def change_basis(structure: Structure,
                 hkl: List[int],
                 fractional_offset: float,
                 folder: str,
                 force: bool = False) -> Tuple[Structure, int]:
    """Modified lattice: (hkl) -> (001) and shift along dhkl."""
    prepared_structure = structure.copy()
    input_h = hkl[0]
    input_k = hkl[1]
    input_l = hkl[2]
    gcd = math.gcd(input_h, input_k, input_l)
    h, k, l = input_h // gcd, input_k // gcd, input_l // gcd
    new_basis_uvw_matrix = get_new_basis(h, k, l)

    save_basis_matrix(folder, new_basis_uvw_matrix, force=force)

    prepared_structure.make_supercell(new_basis_uvw_matrix)
    num_sites = len(prepared_structure)
    # shift all atoms along the third (z) coordinate by fractional_offset
    prepared_structure.translate_sites(range(num_sites), [0, 0, - fractional_offset], frac_coords=True)
    return prepared_structure, gcd


def enlarge_z(structure: Structure, scaling_factor: float) -> Structure:
    # Stretch the cell along the [001] direction while preserving the Cartesian coordinates of the atoms.
    cart_coords = [site.coords for site in structure]  # Obtaining Cartesian coordinates

    # Double the 'c' parameter (change only the third lattice vector)
    new_lattice = structure.lattice.matrix.copy()
    new_lattice[2] = [new_lattice[2][0] * scaling_factor, new_lattice[2][1] * scaling_factor,
                      new_lattice[2][2] * scaling_factor]  # Multiply 'c' by scaling_factor
    logger.info(f"Supercell lattice is {new_lattice}")
    # Create a new structure with new lattice vectors
    new_structure = Structure(
        new_lattice,
        structure.species,
        cart_coords,  # Passing the old Cartesian coordinates
        coords_are_cartesian=True  # Specify that the coordinates are Cartesian (not fractional)
    )
    return new_structure