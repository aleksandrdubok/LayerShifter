"""
Integration tests for layer-shifter processing pipeline.
Uses a real CIF file and compares generated structures with reference files.
"""
import argparse
from pathlib import Path
import pytest
from pymatgen.core import Structure

from layer_shifter.main import run


def test_approach_1_mesh2_hkl_001(tmp_path):
    """
    Run processing for approach 1, mesh 4x4, (10-3) plane, offset -0.5, separation 36.0, cutoff 3.0
    and verify that the output matches the reference structures.
    """
    # ----- Setup: paths and reference files -----
    example_dir = Path(__file__).parent / "data"
    input_cif = example_dir / "PYRZIN22.cif"
    assert input_cif.is_file(), f"Input CIF missing: {input_cif}"

    # Temporary output directory (auto-cleaned by pytest)
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # ----- Build arguments -----
    # Simulating: layer-shifter -i example.cif -o output/ --hkl 0 0 1 --approach 1 --mesh 2 --force
    args = argparse.Namespace(
        input=input_cif,
        output=output_dir,
        hkl=[1, 0, -3],
        offset=-0.5,
        mesh=4,
        separation=36.0,
        approach=1,
        cutoff=3.0,
        force=True,
        debug=False
    )

    # ----- Run the core function -----
    # No log/warning setup needed; run uses current global logging state.
    run(args)

    # ----- Verify output -----
    # Expected files: *a0b0.cif, a0b1, a1b0, ..., a3b3 (16 files)
    generated_cifs = sorted(output_dir.glob("*.cif"))
    assert len(generated_cifs) == 16, f"Expected 16 CIF files, got {len(generated_cifs)}"

    # Compare each generated file with the corresponding reference
    for gen_path in generated_cifs:
        # Extract the suffix like 'a0b0' from the generated filename
        stem = gen_path.stem  # e.g., "PYRZIN22_10m3_a3b3"
        suffix = stem.split('_')[-1]  # "a3b3"
        ref_name = f"PYRZIN22_10m3_{suffix}.cif"
        ref_path = example_dir / ref_name
        assert ref_path.is_file(), f"Reference file missing: {ref_name}"

        # Load and compare structures (tolerance for numerical stability)
        gen_struct = Structure.from_file(str(gen_path))
        ref_struct = Structure.from_file(str(ref_path))
        assert gen_struct.matches(ref_struct, ltol=1e-4, stol=1e-4, angle_tol=1e-4), \
            f"Structure mismatch: {gen_path.name} vs {ref_path.name}"

    # Note: tmp_path and all contents are automatically deleted after the test