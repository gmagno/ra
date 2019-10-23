
import argparse
import os
import sys
import pathlib
import signal

from ra import run_simu
from ra import simulation_api
from ra.log import log

## To run tests
from ra.absorption_database import load_matdata_from_mat, get_alpha_s # just to have some absorption data to test
import numpy as np
from ra.room import Geometry, GeometryMat
import matplotlib.pyplot as plt

def sigint_handler(sig, frame):
    log.debug('Interrupted by user with Ctrl+C!')
    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='ra',
        description='Room Acoustics.'
    )
    parser.add_argument(
        '-c', '--cfg-dir',
        help='Path pointing to dir with simulation configuration files.',
        required=True
    )
    args = vars(parser.parse_args())
    log.debug('Parsed arguments: {}'.format(args))
    return args


def main():
    args = parse_args()
    signal.signal(signal.SIGINT, sigint_handler)
    cfgs = run_simu.setup(args['cfg_dir'])
    run_simu.run(cfgs)

    ##### Write some input data here to test the Simulation class ####
    #### algoritm configuration
    alg_configs = {
        'freq': [63.0, 125.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0, 8000.0], #default - user do not access
        'n_rays': 10000,                 # integer only
        'ht_length': 3.0,
        'dt': 0.001,                    #default
        'allow_scattering': 1,          #default - True = 1
        'transition_order': 2,          #default - integer only
        'rec_radius_init': 0.1,         #default
        'allow_growth': 1,              #default - True = 1
        'rec_radius_final': 1.0
    }
    ### air properties
    air_properties = {
        'Temperature': 25,              #default
        'hr': 50.0,                     #default
        'p_atm': 101325.0               #default
    }
    ### Materials
    alpha_list = load_matdata_from_mat(cfgs['sim_cfg']['material'])
    alpha, s = get_alpha_s(cfgs['sim_cfg']['geometry'], cfgs['mat_cfg']['material'], alpha_list)
    geo = GeometryMat(cfgs['sim_cfg']['geometry'], alpha, s)
    ### Geometry setup
    plane_list_blender = []
    for jp in np.arange(0,10):
        plane_list_blender.append(
            {'name': 'Plane num ' + str(jp+1),
            'bbox': False,
            'vertices': geo.planes[jp].vertices,
            'normal': geo.planes[jp].normal,
            'alpha': alpha[jp],
            's': s[jp],
            'area': geo.planes[jp].area # FIXME comment this after. It comes from matlab, but with blender it will be calculated
            }
        )
    ### Receiver dictionary
    recs = [
        {'coord': [18.0, -5.0, 3.0], 'orientation': [0.0, 1.0, 0.0]},
        {'coord': [12.0, 3.0, 2.2], 'orientation': [0.0, 1.0, 0.0]},
        {'coord': [8.0, 7.0, 1.5], 'orientation': [0.0, 1.0, 0.0]},
        {'coord': [21.0, 1.0, 3.6], 'orientation': [0.0, 1.0, 0.0]}
    ]

    ### Sources dictionary
    srcs = [
        {'coord': [3.0, 2.333, 1.2], 'orientation': [1.0, 0.0, 0.0],
        'power_dB': [80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0],
        'eq_dB': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'delay': 0.0},
        {'coord': [3.0, 0.0 , 1.2], 'orientation': [1.0, 0.0, 0.0],
        'power_dB': [80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0],
        'eq_dB': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'delay': 0.0},
    ]

    # sims = simulation_api.Simulation()
    # sims.set_configs(alg_configs)
    # sims.set_air(air_properties)
    # sims.set_geometry(plane_list_blender)
    # sims.set_raydir()
    # print("The number of rays is {}.".format(sims.rays_v.Nrays))
    # sims.set_receivers(recs)
    # sims.set_memory_init()
    # sims.set_sources(srcs)
    # ## Calculations
    # sims.run_statistical_reverberation() # there can be a separate buttom for this calculation and a window do display the results.
    # # sims.statistical_revtime.plot_t60()
    # sims.run_raytracing()
    # print("Finished the ray tracing.")
    # print("I'll calc intensity")
    # sims.run_intensitycalc()
    # # sims.sr_results[0].plot_edt()
    # sims.stats.plot_c80_f(plotsr = True)
    # plt.show()


if __name__ == '__main__':
    main()
