import structure_factor as sf
import numpy as np

coordinates = np.loadtxt("positions.csv", delimiter=",", dtype=float)
sf.calculate_structure_factor(coordinates, 100, 100, 100, 2*np.pi/1)