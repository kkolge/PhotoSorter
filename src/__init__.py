from pathlib import Path
import sys

def setup_paths():
    """Set up paths for package discovery."""
    current_dir = Path(__file__).parent.absolute()
    sys.path.insert(0, str(current_dir))

setup_paths()