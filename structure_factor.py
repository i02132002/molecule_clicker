import freud
import numpy as np
import matplotlib.pyplot as plt
def calculate_structure_factor(coordinates, Lx, Ly, bins, k_max, k_min=0):
    """Calculates structure factor via the freud library.
    
    Parameters:
    -----------
    coordinates : float, ndarray
        NumPy array of shape (N,2) of particle coordinates.
        
    Lx : float
        Length of system box along the x-dimension.
        
    Ly : float
        Length of system box along the y-dimension.
        
    bins : unsigned int
        Number of bins in k-space.
        
    k_max : float
        Maximum k value to include in the calculation.
        
    k_min : float, optional
        Minimum k value included in the calculation. Note that there are 
        practical restrictions on the validity of the calculation in the 
        long wavelength regime (Default value = 0).
        
    Returns:
    -----------
    bin_edges : float, ndarray
        The edges of each bin of k (x-dimension values for plot).
        
    sf_values : float, ndarray
        Static structure factor S(k) values (y-dimension values for plot).
        
    """
    box, points = transform_box_points(coordinates, Lx, Ly)
    sf = freud.diffraction.StaticStructureFactorDirect(bins=bins, k_max=k_max, k_min=k_min)
    sf.compute(system=(box, points))
    bin_edges = sf.bin_edges[:-1]
    sf_values = sf.S_k
    return [bin_edges, sf_values]

def transform_box_points(coordinates, Lx, Ly):
    new_coordinates = coordinates - np.array([Lx / 2., Ly / 2.])
    points = np.concatenate([new_coordinates, np.zeros((new_coordinates.shape[0], 1))], axis=1)
    box = freud.Box.cube(L=min(Lx, Ly))
    return box, points

def plot_structure_factor(coordinates, Lx, Ly):
    #coordinates = np.loadtxt(filename, delimiter=",", dtype=float)
    box, coordinates = transform_box_points(coordinates, Lx, Ly)
    dp = freud.diffraction.DiffractionPattern(grid_size=2048)
    dp.compute((box, coordinates), zoom=4, peak_width = 0.1)
    img = dp.to_image(vmin=0.1*dp.N_points, vmax=0.7*dp.N_points)
    plt.imshow(img)
    plt.show()