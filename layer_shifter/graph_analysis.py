import networkx as nx
import numpy as np
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.core import Structure
import logging
logger = logging.getLogger(__name__)
from typing import List, Tuple, Optional, Set

def create_structure_graph(structure: Structure,
                           search_cutoff: float) -> StructureGraph:
    """Create a structure graph using CrystalNN."""
    cnn = CrystalNN(
        search_cutoff=search_cutoff,  # Maximum distance for link search
        cation_anion=False  # Ignore charges
    )

    return StructureGraph.from_local_env_strategy(structure, cnn)


def convert_to_nx_graph(structure: Structure,
                        structure_graph: StructureGraph) -> nx.Graph:
    """Convert a StructureGraph to a NetworkX graph."""
    nx_graph = nx.Graph()
    for node in structure_graph.graph.nodes:
        nx_graph.add_node(node, species=str(structure[node].species))

    for u, v, d in structure_graph.graph.edges(data=True):
        nx_graph.add_edge(u, v, **d)

    return nx_graph


def analyze_molecules(nx_graph: nx.Graph) -> List[Set[int]]:
    """Return molecules (connected components of the full graph)."""
    molecules = list(nx.connected_components(nx_graph))
    return molecules


def unite_the_molecular_fragments(nx_graph: nx.Graph,
                                  molecules: List[Set[int]],
                                  structure: Structure) -> Structure:
    """Translate atoms of a molecule into one cell, removing artificial cuts."""
    nx_graph_unperiodic = nx_graph.copy()
    united_structure = structure.copy()
    for molecule in molecules:
        reference_atom = min(molecule)
        nx_graph_unperiodic.nodes[reference_atom]['uvw'] = np.array([0, 0, 0])
        dfs_atom_dict = nx.dfs_successors(nx_graph_unperiodic, source=reference_atom)
        # print(dfs_atom_dict)
        for atom in dfs_atom_dict:
            for next_atom in dfs_atom_dict[atom]:
                # print(atom, next_atom, nx_graph_unperiodic[atom][next_atom]["to_jimage"])
                nx_graph_unperiodic.nodes[next_atom]['uvw'] = nx_graph_unperiodic.nodes[atom]['uvw'] + np.sign(
                    next_atom - atom) * np.array(list(nx_graph_unperiodic[atom][next_atom]["to_jimage"]))
    # print(nx_graph_unperiodic.nodes.data())
    for atom in list(nx_graph_unperiodic.nodes):
        united_structure.translate_sites(atom, nx_graph_unperiodic.nodes[atom]['uvw'], True, False)
        # print(atom, nx_graph_unperiodic.nodes[atom]['uvw'], structure[atom], united_structure[atom])

    return united_structure


def calculate_centers_of_mass(structure: Structure,
                              molecules: List[Set[int]]) -> List[np.ndarray]:
    centers_of_mass = []

    for mol_id, mol_atoms in enumerate(molecules, 1):
        mol_coords = []
        mol_masses = []

        for atom_idx in mol_atoms:
            atom = structure[atom_idx]
            mol_coords.append(atom.coords)
            mol_masses.append(atom.species.weight)  # Atomic mass

        # Convert to NumPy arrays and calculate the center of mass
        coords = np.array(mol_coords)
        masses = np.array(mol_masses)
        com = np.average(coords, axis=0, weights=masses)
        centers_of_mass.append(com)

        # print(f"Molecule {mol_id}: Center of mass = {com}")

    return centers_of_mass


#Additional non-used functions
def visualize_graph(nx_graph: nx.Graph) -> None:
    from matplotlib import pyplot as plt
    """Visualize the graph using matplotlib."""
    plt.figure(figsize=(12, 8))
    nx.draw(nx_graph, with_labels=True, node_color="lightblue", font_size=8)
    plt.title("Molecular graph of the structure")
    plt.show()


def check_periodic_bonds(structure_graph: StructureGraph) -> None:
    """Print inter-cell bonds."""
    for u, v, d in structure_graph.graph.edges(data=True):
        if "to_jimage" in d and d["to_jimage"] != (0, 0, 0):
            logger.info("Bond between %s and %s via periodicity: %s", u, v, d['to_jimage'])


def analyze_fragments(nx_graph: nx.Graph) -> List[Set[int]]:
    """Return fragments after removing edges between periodic images."""
    nx_graph_unperiodic = nx_graph.copy()
    for u, v in nx_graph.edges():
        if nx_graph[u][v]["to_jimage"] != (0, 0, 0):
            nx_graph_unperiodic.remove_edge(u, v)
    fragments = list(nx.connected_components(nx_graph_unperiodic))
    return fragments