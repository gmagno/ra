import scipy.io as spio
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import ra_cpp

def main():
    # mat = spio.loadmat('home/eric/dev/pyc1/example/sphere_test.mat')
    # time_mat = mat['sphere']['time']
    # print('The time from matlab is {} [s]'.format(time_mat))

    ray_origin = np.array([1.810203599838632, 5.429646450941654, 5.08]) #np.array([3.149, 8.1889, 4.85]) #
    v_dir = np.array([0.109294395115118, 0.091255592278199, -0.989811675054591])
    rec_coord = np.array([2.0, 6.0, 1.2])
    rec_radius = 0.5
    c0 = 344.343399967041688
    dist_travel = 136.3016

    # ray_origin = np.array([1.5, 3.5, 1.5])
    # v_dir = np.array([0.1948, 0.9739, -0.1169])
    # rec_coord = np.array([2.0, 6.0, 1.2])
    # rec_radius = 0.1
    # c0 = 344.34
    # dist_travel = 0.0


    time_cross = ra_cpp._raysphere(ray_origin, v_dir, rec_coord, rec_radius, c0, dist_travel)
    
    print("The time cross is {}.".format(time_cross))
    
    time_cross_exp = 0.0075



if __name__ == '__main__':
    main()