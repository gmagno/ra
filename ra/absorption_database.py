import numpy as np
import matplotlib.pyplot as plt
import scipy.io as spio

from log import log

def load_matdata_from_mat(mat_cfg):
    '''
    This function is used to load the database from a .mat file
    '''
    mat = spio.loadmat(mat_cfg['mat_database'],
            struct_as_record = True)
    alpha_list = mat['material']['alpha'][0][0]
    return alpha_list
    # name  = mat['material']['description'][0][0]


def get_alpha_s(geo_cfg, mat_cfg, alpha_list):
    '''
    This function is used to assign the correct absorption and scattering
    coefficients to the planes in the room geometry
    '''
    # Assign from database
    alpha = []
    s = []
    for m in mat_cfg:
        id = m['id']
        alpha.append(alpha_list[id-1])
        s.append(m['s'])
    # Discover how many planes in geometry
    # log.info("alpha before")
    # log.info(alpha)
    # log.info("s before")
    # log.info(s)

    mat = spio.loadmat(geo_cfg['room'],
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
    # log.info("alpha later")
    # log.info(alpha)
    # log.info("s later")
    # log.info(s)
    # alpha = np.array(alpha, dtype = np.float32)
    return alpha, s


def get_alpha_s2(geo_cfg, mat_cfg, alpha_list):
    """ Assign the correct absorption and scattering to each surface

    Parameters
    ----------
    alpha_list : numpy ndarray
        a large matrix containing the absorption spectra on each row.

    mat_cfg : lis of dictionaries
        each entry in the list contains the id and scattering coefficient of a polygon

    geo_cfg : str
        path to geometry file
    """

    # Assign from database
    alpha = []
    s = []
    for m in mat_cfg:
        id = m['id']
        alpha.append(alpha_list[id-1])
        s.append(m['s'])
    # Discover how many planes in geometry
    # log.info("alpha before")
    # log.info(alpha)
    # log.info("s before")
    # log.info(s)

    # mat = spio.loadmat(geo_cfg['room'],
    #     struct_as_record = True)
    # N_planes = len(mat['geometry']['plane'][0][0][0])
    # # Discover how many planes have been assigend already
    # N_assigned_planes = len(s)
    # # Fill the remaining alphas
    # # absorption = alpha_list[9] # 10% absorption
    # # scat = 0.05
    # for jp in np.arange(N_assigned_planes, N_planes):
    #     alpha.append(alpha_list[9])
    #     s.append(0.05)
    # log.info("alpha later")
    # log.info(alpha)
    # log.info("s later")
    # log.info(s)
    # alpha = np.array(alpha, dtype = np.float32)
    return alpha, s