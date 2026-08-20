# Layer Shifter — layer displacement utility for layered crystals

A tool for computational studies of flexible layered crystals. It transforms the crystal structure so that a given `(hkl)` plane becomes parallel to `(001)`, then generates a mesh of structures with shifted layers using three different approaches.

# LayerShifter – Installation Guide

This guide will help you install LayerShifter (even if you are not a developer).  
Choose the method that feels easiest for you: **using Git** or **downloading the ZIP file**.

## Prerequisites (what you need before you start)

- **Python 3.8 or newer** installed on your computer.  
  *To check:* open a terminal (Command Prompt on Windows, Terminal on Mac/Linux) and type:
  ```bash
  python --version
  ```
  or
  ```bash
  python3 --version
  ```
  If you see something like `Python 3.9.7`, you are ready.

- **On Debian/Ubuntu Linux** you may need an extra package. If you later get an error about `venv`, run these two commands (your password will be asked):
  ```bash
  sudo apt update
  sudo apt install python3-venv
  ```
  *What happens:* The system updates its package list and installs the required `python3-venv` package. After that you can create virtual environments without problems.
- For the graphical interface (GUI) on **Debian/Ubuntu Linux**, you may also need to install python3-tk:
  ```bash
  sudo apt install python3-tk
  ```
This package provides the Tk library that PySimpleGUI uses.
## Method 1: Install using Git (automatic, recommended if you have Git)

1. **Open a terminal** (Command Prompt on Windows, Terminal on Mac/Linux).
2. **Download the project:**
   ```bash
   git clone https://github.com/aleksandrdubok/LayerShifter/
   ```
   *What happens:* Git creates a folder called `LayerShifter` and copies all the files into it.
3. **Enter the folder:**
   ```bash
   cd LayerShifter
   ```
4. **Create a virtual environment** (a clean, isolated Python setup just for this tool):
   ```bash
   python -m venv venv
   ```
   *What happens:* A new folder `venv` appears. It contains its own Python and pip. The command is silent if successful.
5. **Activate the virtual environment:**
   - **Linux / Mac:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows (Command Prompt):**
     ```cmd
     venv\Scripts\activate
     ```
   *What happens:* Your terminal prompt changes and now begins with `(venv)`. For example:
   ```
   (venv) C:\Users\YourName\LayerShifter>
   ```
   This means you are inside the virtual environment.
6. **Install the tool and all its dependencies:**
   ```bash
   pip install -e .
   ```
   *What happens:* pip reads the project files, downloads the required packages, and installs a command called `layer-shifter`. You will see output ending with `Successfully installed ...`. Red errors? Make sure you are in the virtual environment and your internet connection is working.
7. **Check that everything works:**
   ```bash
   layer-shifter --help
   ```
   *What should happen:* A help message appears, showing you how to use the program. If you see a “command not found” error, try closing and reopening the terminal, re‑activate the virtual environment, and run the command again.


## Method 2: Install from ZIP (no Git needed)

If you do not have Git or you prefer a simpler download, follow these steps.

1. Go to the project page:  
   [https://github.com/aleksandrdubok/LayerShifter](https://github.com/aleksandrdubok/LayerShifter)
2. Click the green **Code** button, then choose **Download ZIP**.
3. Save the `.zip` file somewhere easy to find (Desktop, Downloads, etc.).
4. **Extract the ZIP:**
   - **Windows:** Right‑click the ZIP file → “Extract All…” → choose a folder and click “Extract”.
   - **Mac:** Double‑click the ZIP file – a folder will appear next to it.
   - **Linux:** Use your file manager (right‑click → “Extract Here”) or in a terminal: `unzip LayerShifter-main.zip`.
5. After extraction you will have a folder named something like `LayerShifter-main`. **Open that folder.**
6. Now you need to **open a terminal inside that folder** (we still need the terminal for the remaining steps, but we skipped the Git part):
   - **Windows:**
     Open the folder in File Explorer. Hold the **Shift** key and **right‑click** on an empty space inside the folder. Choose **“Open command window here”**.  
     *(If you see “Open PowerShell window here” instead, you can use that too – the commands below will work exactly the same.)*
   - **Mac:**
     Right‑click the folder and select **“New Terminal at Folder”** (if available). Otherwise, open the Terminal app, type `cd ` (with a space after `cd`), then drag the `LayerShifter-main` folder into the Terminal window and press Enter.
   - **Linux:**
     Most file managers let you right‑click inside the folder and choose **“Open in Terminal”**. If not, open a terminal and type `cd /path/to/LayerShifter-main`.
7. Once the terminal is open **inside the `LayerShifter-main` folder**, you are exactly where you would have been after step 3 of Method 1.  
   Now follow the same steps 4 to 7 from Method 1:

   - **Create the virtual environment:**
     ```bash
     python -m venv venv
     ```
   - **Activate it:**
     - Linux/Mac: `source venv/bin/activate`
     - Windows: `venv\Scripts\activate`
   - **Install the tool:**
     ```bash
     pip install -e .
     ```
   - **Test it:**
     ```bash
     layer-shifter --help
     ```

   *Remember:* after activating, your prompt must show `(venv)`. That is how you know you are in the right place.
   

## How to use LayerShifter later

Every time you open a new terminal and want to use the program:

1. Navigate to the project folder (where `venv` is):
   ```bash
   cd /path/to/LayerShifter   # or LayerShifter-main
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows (Command Prompt)
   ```
3. You can now run `layer-shifter` commands.  
   When you are finished, type `deactivate` to leave the virtual environment.

That’s it! You have successfully installed LayerShifter.

## Graphical User Interface (GUI)
If you run layer-shifter without any arguments, the program launches a simple graphical interface. This interface lets you:

- Select the input CIF file and output folder using file dialogs.

- Enter Miller indices (HKL), offset, mesh size, separation, and cutoff.

- Choose the displacement approach (1, 2, or 3).

- Enable debug mode or force overwriting of existing files.

- Run the processing and see progress messages in a log area.

To start the GUI:

```bash
layer-shifter
```
On Linux, make sure python3-tk is installed (see prerequisites above). If the GUI does not start, you will see a helpful error message.

You can still use the command-line interface by supplying the usual arguments (see below). 

## Running tests

Install development dependencies:
```bash
pip install -e .[dev]
```

Run all tests:

```bash
pytest tests/
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

**Simple layer displacement for (10-3) with a 4×4 mesh and 36 Å separation:**
```bash
layer-shifter --output ./examples/output -i ./examples/PYRZIN22.cif  --hkl 1 0 -3 --offset -0.5 --separation 36.0 --cutoff 3.0

```
Results are saved with filenames that include the Miller indices and the mesh coordinates a,b. 
Additional  files are saved for reference: 
- basis_matrix.txt containing [uvw] vectors of transformed basis in each of its rows 
- *_transformed.cif containing initial structure with basis transformation applied  


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
- PySimpleGUI

## Project structure

- `layer_shifter/` — main package
  - `cli.py` — command‑line interface
  - `gui.py` — graphical user interface
  - `config.py` — default values
  - `basis_change.py` — basis transformation
  - `graph_analysis.py` — molecular graph analysis
  - `layer_shifting.py` — layer displacement algorithms
  - `io.py` — CIF read/write
  - `math_utils.py` — Diophantine equation solvers
- `tests/` — tests 
- `pyproject.toml`, `setup.py` — package configuration
- - `examples/` — example .cif files

