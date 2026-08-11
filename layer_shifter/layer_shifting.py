import math
import numpy as np
from pymatgen.core import Structure
from typing import List, Tuple, Optional, Set
from layer_shifter.basis_change import enlarge_z
from layer_shifter.graph_analysis import calculate_centers_of_mass, create_structure_graph, convert_to_nx_graph, \
    analyze_molecules, unite_the_molecular_fragments
from layer_shifter.io import write_structure
from layer_shifter.math_utils import mathematics_rounding
from pathlib import Path


import logging
logger = logging.getLogger(__name__)


def shift_layers(structure: Structure,
                 molecules: List[Set[int]],
                 translation_vector: List[float],
                 gcd: int) -> Structure:
    """Approach 1: place layers on opposite sides of c=0 plane and shift the upper layer."""

    centers_of_mass = calculate_centers_of_mass(structure, molecules)
    shifted_layers_structure = structure.copy()
    shifted_layers_structure.add_site_property("marked", [False] * len(structure))  # we will mark atoms for deletion
    marked_indices = []
    # define layer cropping boundaries
    if gcd == 1 or gcd == 2:
        boundary = 0.5
    else:
        boundary = 1 / gcd
    # Now let's iterate through all the molecules and transform the structure.
    for i in range(len(molecules)):
        molecule = molecules[i]
        fract_center_of_mass = np.array(structure.lattice.get_fractional_coords(centers_of_mass[i]))
        # find the position of the molecule in the range from -0.5 to 0.5 along the c-axis
        translation = mathematics_rounding(fract_center_of_mass[2])
        translated_z_coordinate = fract_center_of_mass[2] - translation
        if translated_z_coordinate > boundary or translated_z_coordinate < - boundary:
            # mark excess atoms to delete them later
            for atom in list(molecule):
                marked_indices.append(atom)
        elif translated_z_coordinate > 0:
            # move the layer above the (001) plane and shift it by the translation vector
            for atom in list(molecule):
                shifted_layers_structure.translate_sites(atom,
                                                         np.array(translation_vector) - np.array([0, 0, translation]),
                                                         True, False)
        elif translated_z_coordinate < 0:
            # move the layer below the (001) plane
            for atom in list(molecule):
                shifted_layers_structure.translate_sites(atom, [0, 0, - translation], True, False)

    # remove the atoms marked earlier
    marked_list = shifted_layers_structure.site_properties["marked"]
    for i in marked_indices:
        marked_list[i] = True
    # Update the 'marked' property in the structure
    shifted_layers_structure.add_site_property("marked", marked_list)

    # 3. Find the indices of all atoms where marked == True.
    indices_to_remove = [i for i, marked in enumerate(shifted_layers_structure.site_properties["marked"]) if marked]

    # 4. Remove the marked atoms.
    shifted_layers_structure.remove_sites(indices_to_remove)

    return shifted_layers_structure


def generate_mesh_approach_1(mesh_size: int, structure: Structure, gcd: int, interlayer_separation_distance: float,
                             output_dir: str, base_name: str, hkl: List[int], search_cutoff: float, force: bool = False) -> None:
    """Generate files for the first approach."""
    if gcd == 1:
        # For (001), two adjacent layers lie in different unit cells; therefore, the unit cell must be doubled in the [001] direction.
        structure.make_supercell([1, 1, 2])

    # Identify them in the molecular structure and connect their fragments.
    structure_graph = create_structure_graph(structure, search_cutoff)
    nx_graph = convert_to_nx_graph(structure, structure_graph)
    molecules = analyze_molecules(nx_graph)
    united_structure = unite_the_molecular_fragments(nx_graph, molecules, structure)

    # Layer shift
    d_hkl = united_structure.lattice.d_hkl([0, 0, 1])
    enlarging_z_factor = int(interlayer_separation_distance/d_hkl + 1/gcd) + 1
    for i in range(mesh_size):
        for j in range(mesh_size):

            translation_vector = [1 / mesh_size * i, 1 / mesh_size * j, 0]
            shifted_structure = shift_layers(united_structure, molecules, translation_vector, gcd)
            # Create a structure in which the layers are spaced at a specified distance.
            enlarged_structure = enlarge_z(shifted_structure, enlarging_z_factor)
            stem = base_name
            hkl_str = ''.join(str(x).replace('-', 'm') for x in hkl)
            output_path = Path(output_dir) / f"{stem}_{hkl_str}_a{i}b{j}"
            write_structure(enlarged_structure, output_path, force=force)
            logger.info("Written: %s", output_path)


def shift_layers_staired_approach(structure: Structure,
                                  molecules: List[Set[int]],
                                  translation_vector: List[float],
                                  gcd: int,
                                  mesh_size: int) -> Structure:
    """Approach 2: stair-like stacking."""
    # takes a pymatgen structure as input,
    # a list of sets containing atom indices for different molecules,
    # translation_vector – a vector [x, y, 0] by which molecules with centers above 0 along the c-axis are shifted,
    # gcd – the GCD of hkl, determining the slice thickness.

    centers_of_mass = calculate_centers_of_mass(structure, molecules)
    shifted_layers_structure = structure.copy()
    # Now let's iterate through all the molecules and transform the structure.
    for i in range(len(molecules)):
        molecule = molecules[i]
        fract_center_of_mass = np.array(structure.lattice.get_fractional_coords(centers_of_mass[i]))
        translation_Z = math.ceil(fract_center_of_mass[2])
        translated_z_coordinate = fract_center_of_mass[2] - translation_Z + 1
        for layer_number in range(mesh_size):
            if (layer_number/mesh_size) <= translated_z_coordinate < (layer_number+1)/mesh_size:
                for atom in list(molecule):
                    shifted_layers_structure.translate_sites(atom, layer_number*np.array(translation_vector) + np.array([0, 0, - translation_Z]),True, False)
    return shifted_layers_structure


def generate_mesh_staired_approach(mesh_size: int, structure: Structure, gcd: int, output_dir: str, base_name: str,
                                   hkl: List[int], search_cutoff: float, force: bool = False) -> None:
    """Generate files for the second approach (stair-like)."""
    if mesh_size // gcd < 1:
        raise ValueError("mesh_size must be >= gcd")
    if mesh_size % gcd != 0:
        raise ValueError("mesh_size must be a multiple of gcd(hkl)")

    supercell_size = mesh_size // gcd
    structure.make_supercell([1, 1, supercell_size])

    # Identify molecules the molecular structure and connect their fragments.
    structure_graph = create_structure_graph(structure, search_cutoff)
    nx_graph = convert_to_nx_graph(structure, structure_graph)
    molecules = analyze_molecules(nx_graph)
    united_structure = unite_the_molecular_fragments(nx_graph, molecules, structure)

    for i in range(mesh_size):
        for j in range(mesh_size):

            translation_vector = [1 / mesh_size * i, 1 / mesh_size * j, 0]
            shifted_structure = shift_layers_staired_approach(united_structure, molecules, translation_vector, gcd, mesh_size)

            stem = base_name
            hkl_str = ''.join(str(x).replace('-', 'm') for x in hkl)
            output_path = Path(output_dir) / f"{stem}_stairsapproach_{hkl_str}_a{i}b{j}"

            write_structure(shifted_structure, output_path, force=force)
            logger.info("Written: %s", output_path)


def shift_layers_staired_approach_inversed_sym(
        structure: Structure,
        molecules: List[Set[int]],
        translation_vector: List[float],
        n_layers: int) -> Structure:
    """Approach 3: stair-like with inversion symmetry (shift only every second layer)."""
    # takes a pymatgen structure as input,
    # a list of sets containing atom indices for different molecules,
    # translation_vector – a vector [x, y, 0] by which molecules with centers above 0 along the c-axis are shifted,
    # gcd – the GCD of hkl, determining the slice thickness.

    centers_of_mass = calculate_centers_of_mass(structure, molecules)
    shifted_layers_structure = structure.copy()

    for i in range(len(molecules)):
        molecule = molecules[i]
        fract_center_of_mass = np.array(structure.lattice.get_fractional_coords(centers_of_mass[i]))

        translation_Z = math.ceil(fract_center_of_mass[2])
        translated_z_coordinate = fract_center_of_mass[2] - translation_Z + 1
        for layer_number in range(n_layers):
            if (layer_number/n_layers) <= translated_z_coordinate < (layer_number+1)/n_layers:
                for atom in list(molecule):
                    shifted_layers_structure.translate_sites(atom, (layer_number+1) % 2 * np.array(translation_vector) + np.array([0, 0, - translation_Z]),True, False)
    return shifted_layers_structure


def generate_mesh_staired_inversed_sym(mesh_size: int, structure: Structure, gcd: int, output_folder: str,
                                       base_name: str, hkl: List[int], search_cutoff: float, force: bool = False) -> None:
    """Generate files for the third approach."""
    n_layers = gcd
    if gcd % 2 == 1:
        structure.make_supercell([1, 1, 2])
        n_layers = gcd * 2

    structure_graph = create_structure_graph(structure, search_cutoff)
    nx_graph = convert_to_nx_graph(structure, structure_graph)
    molecules = analyze_molecules(nx_graph)
    united_structure = unite_the_molecular_fragments(nx_graph, molecules, structure)

    for i in range(mesh_size):
        for j in range(mesh_size):

            translation_vector = [1 / mesh_size * i, 1 / mesh_size * j, 0]
            shifted_structure = shift_layers_staired_approach_inversed_sym(united_structure, molecules, translation_vector, n_layers)

            stem = base_name
            hkl_str = ''.join(str(x).replace('-', 'm') for x in hkl)
            output_path = Path(output_folder) / f"{stem}_invstairsapproach_{hkl_str}_a{i}b{j}"

            write_structure(shifted_structure, output_path, force=force)

            logger.info("Written: %s", output_path)