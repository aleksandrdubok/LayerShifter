from layer_shifter.basis_change import change_basis
from layer_shifter.cli import parse_args
from layer_shifter.io import load_structure
from layer_shifter.layer_shifting import generate_mesh_approach_1, generate_mesh_staired_approach, \
    generate_mesh_staired_inversed_sym
import warnings
import logging


def main():

    args = parse_args()

    if args.mesh <= 0:
        raise ValueError("mesh size must be positive")
    if args.separation < 0:
        raise ValueError("separation must be non-negative")
    if args.cutoff < 0:
        raise ValueError("cutoff must be non-negative")
    if args.hkl == [0, 0, 0]:
        raise ValueError("Miller indices cannot all be zero")

    # Logging and warning settings
    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:

        logging.basicConfig(level=logging.WARNING)

        # Since cifs rarely contain oxidations sites these pymatgen warnings are ignored:
        # UserWarning: No oxidation states specified on sites!
        # For better results, set the site oxidation states in the structure.
        #
        # UserWarning: CrystalNN: cannot locate an appropriate radius, covalent or atomic radii will be used,
        # this can lead to non-optimal results.
        warnings.simplefilter("ignore", DeprecationWarning)
        warnings.simplefilter("ignore", UserWarning)
        warnings.simplefilter("ignore", FutureWarning)

    input_path = args.input.resolve()  
    if args.output:
        output_dir = args.output.resolve()
    else:
        output_dir = input_path.parent

    if not input_path.is_file():
        raise FileNotFoundError(f'Input file is not found {input_path}')
    output_dir.mkdir(parents=True, exist_ok=True)

    input_file_name = input_path.stem


    
    search_cutoff = args.cutoff
    hkl = args.hkl
    fractional_offset = args.offset
    mesh_size = args.mesh
    interlayer_separation_distance = args.separation
    approach = args.approach

    original_structure = load_structure(str(input_path))

    structure, gcd = change_basis(original_structure, hkl, fractional_offset, str(output_dir), force=args.force)

    if approach == 1:
        generate_mesh_approach_1(mesh_size, structure, gcd, interlayer_separation_distance, str(output_dir), input_file_name,
                                 hkl, search_cutoff, force=args.force)
    elif approach == 2:
        generate_mesh_staired_approach(mesh_size, structure, gcd, str(output_dir), input_file_name, hkl, search_cutoff, force=args.force)
    elif approach == 3:
        generate_mesh_staired_inversed_sym(mesh_size, structure, gcd, str(output_dir), input_file_name, hkl, search_cutoff, force=args.force)


if __name__ == "__main__":
    main()
