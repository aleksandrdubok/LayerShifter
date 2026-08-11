import pytest
import warnings

@pytest.fixture(autouse=True)
def suppress_pymatgen_warnings():
    """Suppress known pymatgen warnings during testing."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="No oxidation states specified on sites!.*")
        warnings.filterwarnings("ignore", message="CrystalNN: cannot locate an appropriate radius.*")
        warnings.filterwarnings("ignore", message="We strongly discourage using implicit binary/text `mode`.*")
        yield