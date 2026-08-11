import argparse
from layer_shifter.config import DEFAULT_SEARCH_CUTOFF, DEFAULT_INTERLAYER_DISTANCE, DEFAULT_MESH_SIZE
from pathlib import Path

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments and return the parameters object."""
    parser = argparse.ArgumentParser(
        description='A tool for computational studies of flexible layered crystals that generates structures with shifted layers.'
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 0.0.0"
    )
    parser.add_argument(
        '--output',
        '-o',
        default=None,
        type=Path,
        help='Path to the output folder (required)'
    )
    parser.add_argument(
        '--input',
        '-i',
        required=True,
        type=Path,
        help='Path to the input structure .cif file (required)'
    )
    parser.add_argument(
        '--approach',
        type=int,
        choices=[1, 2, 3],
        default=1,
        help=argparse.SUPPRESS  # Approach selection: 1 – approach_1, 2 – staired, 3 – staired_inversed_sym' - experimental feature
    )
    parser.add_argument(
        '--mesh',
        type=int,
        default=DEFAULT_MESH_SIZE,
        help='Number of points in each mesh direction'
    )
    parser.add_argument(
        '--hkl',
        nargs=3,
        type=int,
        default=[0, 0, 1],
        metavar=('H', 'K', 'L'),
        help='Three integers for hkl indices (e.g. 2 0 -2)'
    )
    parser.add_argument(
        '--offset',
        type=float,
        default=0.0,
        help='Fractional shift (in relative units)'
    )
    parser.add_argument(
        '--separation',
        type=float,
        default=DEFAULT_INTERLAYER_DISTANCE,
        help='Desired interlayer separation (not guaranteed)'
    )

    parser.add_argument(
        '--cutoff',
        type=float,
        default=DEFAULT_SEARCH_CUTOFF,
        help='search_cutoff parameter'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='Enable debug logging and show all warnings.'
    )
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        default=False,
        help='Overwrite existing files without prompting for confirmation'
    )
    return parser.parse_args()