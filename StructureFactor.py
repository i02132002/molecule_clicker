import freud
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class StructureFactorPlotter:
    """Plots the structure factor via the freud library.

           Parameters:
           -----------
           coordinates : float, ndarray
               NumPy array of shape (N,2) of particle coordinates.

           Lx : float
               Length of system box along the x-dimension.

           Ly : float
               Length of system box along the y-dimension.

           """
    def __init__(self, Lx, Ly, coordinates=None, filename=None):
        self.Lx, self.Ly = Lx, Ly
        self.filename = filename
        self.coordinates = None
        if filename != None:
            self.coordinates = self.read_positions()
        else:
            self.coordinates = coordinates

    def calculate_structure_factor(self, bins, k_max, k_min=0):
        """Calculates structure factor via the freud library.

        Parameters:
        -----------
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
        box, points = self.transform_box_points()
        sf = freud.diffraction.StaticStructureFactorDirect(bins=bins, k_max=k_max, k_min=k_min)
        sf.compute(system=(box, points))
        bin_edges = sf.bin_edges[:-1]
        sf_values = sf.S_k
        return [bin_edges, sf_values]

    def transform_box_points(self):
        """Transforms coordinates into point coordinates within a Freud box.
        The center of the box is at (0,0) with maximum values of +/- (Lx/2, Ly/2).

        Returns:
        -----------
        box : freud.Box.cube
            A freud box containing the coordinates of the points.

        points : float, ndarray
            The converted point coordinates by subtracting (Lx/2, Ly/2) from the
            original(x,y) coordinates.

        """
        new_coordinates = self.coordinates - np.array([self.Lx / 2., self.Ly / 2.])
        points = np.concatenate([new_coordinates, np.zeros((new_coordinates.shape[0], 1))], axis=1)
        box = freud.Box.cube(L=min(self.Lx, self.Ly))
        return box, points

    def plot_structure_factor(self, grid_size=2048, zoom=10, save_csv=False):
        """Plots the structure factor given two files <filename>_positions.csv and <filename>.jpg.

               Parameters:
               -----------
               grid_size : unsigned int, optional
                   input and output grid resolution used to produce the structure factor

               zoom : float, optional
                   magnification level of the structure factor plot

               save_csv : bool, optional
                   toggles whether to save the structure factor data to Sq.csv

               Returns:
               -----------
                None
               """
        box, coordinates = self.transform_box_points()
        dp = freud.diffraction.DiffractionPattern(grid_size=grid_size)
        dp.compute((box, coordinates), zoom=zoom, peak_width=0.1)
        img = dp.to_image(vmin=0.01*dp.N_points, vmax=0.6*dp.N_points)
        k_max = np.pi /  self.Lx * grid_size
        plt.imshow(img, origin='lower', extent=[-k_max/zoom, k_max/zoom, -k_max/zoom, k_max/zoom])
        #plt.axis('off')
        if self.filename != None:
            plt.savefig(self.filename + '_structure_factor.png', dpi=1200, bbox_inches='tight')
        plt.show()
        if save_csv:
            np.savetxt('Sq.csv', dp.diffraction, delimiter=",")
    def read_positions(self):
        coordinates = np.loadtxt(self.filename + '_positions.csv', delimiter=",", dtype=float)
        coordinates = np.array(coordinates)
        coordinates = pd.DataFrame(data=coordinates, columns=['x', 'y'])
        return coordinates
    def plot_positions_overlay(self):
        plt.scatter(self.coordinates['x'], self.coordinates['y'], color='r', marker='.')
        img = plt.imread(self.filename + '.jpg')
        plt.imshow(img, extent=[0, self.Lx, 0, self.Ly])
        plt.axis('off')
        plt.savefig(self.filename + '_overlay.png', dpi=1200, bbox_inches='tight')
        plt.show()

