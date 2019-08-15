import math
import codecs
import json

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as spio

import ra_cpp

from ra.rayinidir import RayInitialDirections
from ra.receivers import setup_receivers
from ra.sources import setup_sources
from ra.controlsair import AlgControls, AirProperties
from ra.room import Geometry, GeometryMat
from ra.absorption_database import load_matdata_from_mat, get_alpha_s
from ra.statistics import StatisticalMat
from ra.ray_initializer import ray_initializer
from ra.results import process_results, SRStats

def main():
    path = 'data/legacy/odeon_ex/'          # room folder
    pkl_fname_res = 'odeon_ex'              # simulation results name
    # path = 'data/legacy/ptb_studio_ph1/'    # room folder
    # pkl_fname_res = 'ptb_studio_ph1'        # simulation results name
    # path = 'data/legacy/ptb_studio_ph2/'    # room folder
    # pkl_fname_res = 'ptb_studio_ph2_open'        # simulation results name
    # pkl_fname_res = 'ptb_studio_ph2_close'        # simulation results name
    tml_name_cfg = 'simulation.toml'        # toml configuration file
    tml_name_mat = 'surface_mat_id.toml'    # toml material file
    # tml_name_mat = 'surface_mat_open_id.toml'    # toml material file
    # tml_name_mat = 'surface_mat_close_id.toml'    # toml material file

    ##### Setup algorithm controls ########
    controls = AlgControls(path+tml_name_cfg)

    ##### Setup air properties ########
    air = AirProperties(path+tml_name_cfg)
    air_m = air.air_absorption(controls.freq)

    ##### Setup materials #############
    alpha_list = load_matdata_from_mat(path+tml_name_cfg)
    alpha, s = get_alpha_s(path+tml_name_cfg, path+tml_name_mat, alpha_list)

    ##### Setup Geometry ###########
    geo = GeometryMat(path+tml_name_cfg, alpha, s)
    geo.plot_mat_room(normals = 'on')
    # geo = Geometry('simulation.toml', alpha, s)
    # geo.plot_dae_room(normals = 'on')

    ##### Statistical theory ############
    res_stat = StatisticalMat(geo, controls.freq, air.c0, air_m)
    res_stat.t60_sabine()
    res_stat.t60_eyring()
    # res_stat.t60_kutruff(gamma=0.4)
    # res_stat.t60_araup()
    # res_stat.t60_fitzroy()
    # res_stat.t60_milsette()
    # res_stat.plot_t60()

    ##### ray's initial direction ########
    rays_i_v = RayInitialDirections()
    # rays_i_v.single_ray([0.0, -1.0, 0.0])#([0.7236, -0.5257, 0.4472])
    rays_i_v.isotropic_rays(controls.Nrays) # 15
    # mat = spio.loadmat('ra/vin_matlab.mat')
    # rays_i_v.vinit = mat['vin']
    # rays_i_v.random_rays(1000)
    # rays_i_v.single_ray(rays_i_v.vinit[41])
    print("The number of rays is {}.".format(rays_i_v.Nrays))

    ##### Setup receiver, reccross and reccrossdir ########
    receivers, reccross, reccrossdir = setup_receivers(path+tml_name_cfg)

    #### Allocate some memory in python for geometrical ray tracing ########################
    # Estimate max reflection order
    N_max_ref = math.ceil(1.5 * air.c0 * controls.ht_length * \
        (geo.total_area / (4 * geo.volume)))
    # Allocate according to max reflection order
    rays = ray_initializer(rays_i_v, N_max_ref, controls.transition_order, reccross)

    ##### Setup sources - ray history goes inside source object ########
    sources = setup_sources(path+tml_name_cfg, rays, reccrossdir)

    ############# Now - the calculations ####################
    ############### direct sound ############################
    sources = ra_cpp._direct_sound(sources, receivers, controls.rec_radius_init,
        geo.planes, air.c0, rays_i_v.vinit)

    ############### ray tracing ##############
    sources = ra_cpp._raytracer_main(controls.ht_length,
        controls.allow_scattering, controls.transition_order,
        controls.rec_radius_init, controls.alow_growth, controls.rec_radius_final,
        sources, receivers, geo.planes, air.c0,
        rays_i_v.vinit)

    ######## Calculate intensities ###################
    sources = ra_cpp._intensity_main(controls.rec_radius_init,
        sources,air.c0,air.m, res_stat.alphas_mtx)

    ########### Process reflectograms and acoustical parameters #####################
    sou = process_results(controls.Dt, controls.ht_length,
        controls.freq, sources, receivers)

    ########## Statistics ##########################################################
    stats = SRStats(sou)
    ######## some plotting ##############################
    sou[0].plot_single_reflecrogram(band = 4, jrec = 2)
    sou[0].plot_single_reflecrogram(band = 4, jrec = 1)
    # sou[0].plot_decays()
    # sou[0].plot_edt()
    # sou[0].plot_t20()
    # sou[0].plot_t30()
    # sou[0].plot_c80()
    # sou[0].plot_d50()
    # sou[0].plot_ts()
    # sou[0].plot_g()
    # print(sources[0].rays[0].refpts_hist)
    print(sources[0].reccrossdir[0].cos_dir)
    ############# Save trial #########################
    import pickle
    with open(path+pkl_fname_res+'.pkl', 'wb') as output:
        pickle.dump(res_stat, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(sou, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(stats, output, pickle.HIGHEST_PROTOCOL)
        # pickle.dump(geo, output, pickle.HIGHEST_PROTOCOL)


        # pickle.dump(sources, output, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
