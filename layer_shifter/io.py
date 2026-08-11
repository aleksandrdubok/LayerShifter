import numpy as np
from pymatgen.core import Structure
from pathlib import Path
import sys
import logging
logger = logging.getLogger(__name__)

def save_basis_matrix(output_dir: str, new_basis_uvw_matrix: np.ndarray, force: bool = False) -> None:
    """
    Save the new basis matrix to a text file.
    If the file already exists and force is False, ask the user for confirmation.
    """
    path = Path(output_dir) / 'basis_matrix.txt'
    if path.exists() and not force:
        answer = input(f"File '{path}' already exists. Overwrite? [y/N] ")
        if answer.lower() not in ('y', 'yes'):
            print("Skipped saving basis matrix.", file=sys.stderr)
            return
    with open(path, 'w') as f:
        f.write("new basis [u,v,w] matrix is: \n")
        np.savetxt(f, new_basis_uvw_matrix, fmt='%i')
    logger.info(f"basis matrix is saved to basis_matrix.txt")


def load_structure(filename: str) -> Structure:
    """Load a structure from a CIF file."""
    structure = Structure.from_file(filename)
    return structure


def write_structure(structure: Structure, path: Path, force: bool = False) -> bool:
    """
    Write the structure to a CIF file. Extension .cif is added automatically.
    Returns True if the file was written, False if skipped.
    """
    out_path = path.with_suffix('.cif')
    if out_path.exists() and not force:
        answer = input(f"File '{out_path}' already exists. Overwrite? [y/N] ")
        if answer.lower() not in ('y', 'yes'):
            print(f"Skipped '{out_path.name}'", file=sys.stderr)
            return False
    structure.to(filename=str(out_path))
    logger.info(f"Structure uploaded: {structure.formula}")
    return True


