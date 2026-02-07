import sys
from pathlib import Path

# Make the local package importable without installation.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from melk import mElk

def main():
    # Convert ELK JSON output to SVG
    elk_svg = mElk.from_file("examples/sample2.layout.json")
    elk_svg.write("examples/sample2.svg")

if __name__ == "__main__":
    main()
