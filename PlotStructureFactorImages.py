import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from StructureFactor import *
import sys

def main():
    try:
        FILENAME = sys.argv[1]
        SCAN_SIZE = float(sys.argv[2])
    except IndexError:
        print('Missing some arguments: filename, scan_size_nm, n_pixels')
        return
    filename = 'test'
    Lx, Ly = SCAN_SIZE, SCAN_SIZE
    sfp = StructureFactorPlotter(Lx, Ly, filename=filename)
    sfp.plot_positions_overlay()
    sfp.plot_structure_factor()

if __name__ == "__main__":
    main()
