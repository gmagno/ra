import toml
from ra.controlsair import load_cfg
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as spio


def load_matdata_from_mat(config_file):
    '''
    This function is used to load the database from a .mat file
    '''
    config = load_cfg(config_file)
    mat = spio.loadmat(config['material']['mat_database'],
            struct_as_record = True)
    alpha_list = mat['material']['alpha'][0][0]
    return alpha_list
    # name  = mat['material']['description'][0][0]

def get_alpha_s(geo_file, mat_file, alpha_list):
    '''
    This function is used to assign the correct absorption and scattering
    coefficients to the planes in the room geometry
    '''
    # Assign from database
    config = load_cfg(mat_file)
    alpha = []
    s = []
    for m in config['material']:
        id = m['id']
        alpha.append(alpha_list[id-1])
        s.append(m['s'])
    # Discover how many planes in geometry
    # print("alpha before")
    # print(alpha)
    # print("s before")
    # print(s)
    
    config = load_cfg(geo_file)
    mat = spio.loadmat(config['geometry']['room'],
        struct_as_record = True)
    N_planes = len(mat['geometry']['plane'][0][0][0])
    # Discover how many planes have been assigend already
    N_assigned_planes = len(s)
    # Fill the remaining alphas
    # absorption = alpha_list[9] # 10% absorption
    # scat = 0.05
    for jp in np.arange(N_assigned_planes, N_planes):
        alpha.append(alpha_list[9])
        s.append(0.05)
    # print("alpha later")
    # print(alpha)
    # print("s later")
    # print(s)
    # alpha = np.array(alpha, dtype = np.float32)
    return alpha, s