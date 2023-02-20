import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from StructureFactor import *

def main():
    filename = 'test'
    Lx, Ly = 20, 20
    sfp = StructureFactorPlotter(Lx, Ly, filename=filename)
    sfp.plot_positions_overlay()
    sfp.plot_structure_factor()

if __name__ == "__main__":
    main()
