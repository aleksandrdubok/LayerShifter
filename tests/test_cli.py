from layer_shifter.cli import parse_args
import sys
from pathlib import Path

def test_defaults():
    sys.argv = ["prog", "-o", "./", "-i", "./test.cif"]
    args = parse_args()
    assert args.output == Path("./")
    assert args.input == Path("./test.cif")
    assert args.hkl == [0,0,1]

