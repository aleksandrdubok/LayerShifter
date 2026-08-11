# Layer Shifter — layer displacement utility for layered crystals

A tool for computational studies of flexible layered crystals. It transforms the crystal structure so that a given `(hkl)` plane becomes parallel to `(001)`, then generates a mesh of structures with shifted layers using three different approaches.
## Prerequisites

- Python 3.8 or higher
- On **Debian/Ubuntu** systems, you may need to install the `python3-venv` package if it is not already present:
  ```bash
  sudo apt update
  sudo apt install python3-venv
  
## Installation

1. Clone the repository:
   
   ```bash
   git clone https://github.com/aleksandrdubok/LayerShifter/
   cd layer_shifter
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
3. Install the package and dependencies:
   ```bash
   pip install -e .
   ```
4. Verify the installation:
   ```bash
   layer-shifter --help
   ```

## Usage

Required arguments:

- `--input`,  `-i`  — path to the input CIF file.

Optional parameters:



| Parameter          | Default     | Description |
|--------------------|-------------|-------------|
|`--output`, `-o`        | Parent dir of `--input`| Output path. The input file parent folder is set as output path by default| 
| `--hkl`            | `0 0 1`     | Miller indices of the plane to be made perpendicular to the z‑axis |
| `--offset`         | `0.0`       | Additional shift of all atoms along the new z direction (in fractions of d_hkl) |
| `--mesh`           | `4`         | Size of the displacement grid in the ab plane (mesh × mesh) |
| `--separation`     | `36.0`      | Desired interlayer distance in Å (stretches the c period) |
| `--approach`       | `1`         | Displacement approach: `1` – basic, `2` – stair-like, `3` – inversion‑symmetric stair-like |
| `--cutoff`         | `3.0`       | Maximum distance for bond search (CrystalNN) |
| `--debug`          | `False`     | Enable verbose logging and show all warnings |
 `--force`, `-f`           | `False`     | Enable overwriting existing files without prompting for confirmation |

### Examples

**Simple layer displacement for (001) with a 5×5 mesh and 40 Å separation:**
```bash
layer-shifter --output ./001_0 -i ./phase.cif --approach 1 --mesh 5 --separation 40
```

**Stair‑like displacement along the (100) plane:**
```bash
layer-shifter --output ./100_0_stair -i ./phase.cif --hkl 1 0 0 --approach 2 --mesh 4
```

**Same, with debug output:**
```bash
layer-shifter --output ./100_0_stair -i ./phase.cif --hkl 1 0 0 --approach 2 --mesh 4 --debug
```

Results are saved with filenames that include the Miller indices and the mesh coordinates a,b.

## How it works

1. **Basis change.** The `(hkl)` plane is transformed into `(001)` of a new cell using a transformation matrix. An optional offset along the new z‑axis is applied.
2. **Molecular graph construction.** Based on CrystalNN, bonds are determined, a graph of the structure is built, and connected components (molecules/layers) are identified.
3. **Fragment reunification.** Periodic breaks are removed — all atoms belonging to the same molecule are moved into a single unit cell.
4. **Mesh generation.** For each grid point (a,b), layers are shifted by a vector `(a/mesh, b/mesh, 0)` according to the chosen approach:
   - **Approach 1** – all layers above the `z=0` plane are displaced by the given vector; layers below remain in place; excess copies are trimmed.
   - **Approach 2 (stair‑like)** – each layer receives a fraction of the displacement proportional to its z coordinate.
   - **Approach 3 (inversion‑symmetric)** – the same stair‑like scheme, but the vector is applied only to every other layer.
5. **Interlayer distance enlargement.** If requested, the c lattice parameter is stretched so that the gap between layers reaches the specified value.

## Dependencies

- Python ≥ 3.8
- pymatgen
- networkx
- numpy
- matplotlib

## Project structure

- `layer_shifter/` — main package
  - `cli.py` — command‑line interface
  - `config.py` — default values
  - `basis_change.py` — basis transformation
  - `graph_analysis.py` — molecular graph analysis
  - `layer_shifting.py` — layer displacement algorithms
  - `io.py` — CIF read/write
  - `math_utils.py` — Diophantine equation solvers
- `tests/` — tests (under development)
- `pyproject.toml`, `setup.py` — package configuration

## Running tests

Install development dependencies:
```bash
pip install -e .[dev]
```

Run all tests:

```bash
pytest tests/
```