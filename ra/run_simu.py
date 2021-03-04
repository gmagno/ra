import argparse
import codecs
import json
import math
import os
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as spio
import toml

from log import log
from rayinidir import RayInitialDirections
from receivers import setup_receivers
from sources import setup_sources
from controlsair import AlgControls, AirProperties, save_sim
from room import Geometry, GeometryMat
from absorption_database import load_matdata_from_mat, get_alpha_s
from statistics import StatisticalMat
from ray_initializer import ray_initializer
from results import process_results, SRStats
import ra_cpp


def load_cfg(cfgfile):
    '''
    Function to load and read the toml file
    '''
    with open(cfgfile, 'r') as f:
        config = toml.loads(f.read())
    return config


def setup(cfg_dir):
    ################ ODEON EXAMPLE #####################################
    # pkl_fname_res = 'odeon_ex'              # simulation results name
    tml_name_cfg = 'simulation.toml'        # toml configuration file
    tml_name_mat = 'surface_mat_id.toml'    # toml material file
    ############# PTB phase 1 #########################################
    # pkl_fname_res = 'ptb_studio_ph1'        # simulation results name
    # tml_name_cfg = 'simulation.toml'        # toml configuration file
    # tml_name_mat = 'surface_mat_id.toml'    # toml material file
    ############### PTB phase 2 #######################################
    # path = '/home/eric/dev/ra/data/legacy/ptb_studio_ph2/'
    # pkl_fname_res = 'ptb_studio_ph2_open'        # simulation results name
    # pkl_fname_res = 'ptb_studio_ph2_close'        # simulation results name
    # tml_name_cfg = 'simulation.toml'        # toml configuration file
    # tml_name_cfg = 'simulation_odeon.toml'        # toml configuration file
    # tml_name_mat = 'surface_mat_open_id.toml'    # toml material file
    # tml_name_mat = 'surface_mat_open_id_scte.toml'    # toml material file
    # tml_name_mat = 'surface_mat_close_id.toml'    # toml material file
    # tml_name_mat = 'surface_mat_open_id_odeon_scte.toml'    # toml material file
    ############### PTB phase 3 #######################################
    # pkl_fname_res = 'ptb_studio_ph3_open'              # simulation results name
    # pkl_fname_res = 'ptb_studio_ph3_close'              # simulation results name
    # tml_name_cfg = 'simulation_ptb_ph3.toml'        # toml configuration file
    # tml_name_cfg = 'simulation_ptb_ph3_odeon.toml'        # toml configuration file
    # pkl_fname_res = 'ptb_studio_ph3_open'              # simulation results name
    # pkl_fname_res = 'ptb_studio_ph3_close'              # simulation results name
    # tml_name_cfg = 'simulation_ptb_ph3.toml'        # toml configuration file
    # tml_name_mat = 'surface_mat_open_id.toml'    # toml material file
    # tml_name_mat = 'surface_mat_id_ptb_ph3_c.toml'    # toml material file
    # tml_name_mat = 'surf_mat_ptb_ph3_o_4kHz.toml'    # toml material file
    # tml_name_mat = 'surface_mat_id_ptb_ph3_o.toml'    # toml material file
    #tml_name_mat = 'surface_mpathat_id_ptb_ph3_c.toml'    # toml material file
    # tml_name_mat = 'surface_pathmat_id_ptb_ph3_o_odeon.toml'    # toml material file
    # tml_name_mat = 'surface_mat_id_ptb_ph3_o_odeon_scte.toml'    # toml material file

    #################### Elmia ##########################################
    # pkl_fname_res = 'elmia_odeon'        # simulation results name
    # tml_name_cfg = 'simulation_elmia_odeon.toml'        # toml configuration file
    # tml_name_cfg = 'simulation_elmia.toml'        # toml configuration file
    # tml_name_mat = 'surface_mat_id_elmia_odeon.toml'    # toml material file
    # tml_name_mat = 'surface_mat_id_elmia.toml'    # toml material file

    cfgs = {
        'sim_cfg': load_cfg(pathlib.Path(cfg_dir) / tml_name_cfg),
        'mat_cfg': load_cfg(pathlib.Path(cfg_dir) / tml_name_mat)
    }
    return cfgs


def run(cfgs):
    ##### Setup algorithm controls ########
    # FIXME: use pathlib instead of string concatenation
    controls = AlgControls(cfgs['sim_cfg']['controls'])

    ##### Setup air properties ########
    air = AirProperties(cfgs['sim_cfg']['air'])
    air_m = air.air_absorption(controls.freq)

    ##### Setup materials #############
    alpha_list = load_matdata_from_mat(cfgs['sim_cfg']['material'])
    alpha, s = get_alpha_s(cfgs['sim_cfg']['geometry'], cfgs['mat_cfg']['material'], alpha_list)

    ##### Setup Geometry ###########
    geo = GeometryMat(cfgs['sim_cfg']['geometry'], alpha, s)
    geo.plot_mat_room(normals = 'on')
    # geo = Geometry('simulation.toml', alpha, s)
    # geo.plot_dae_room(normals = 'on')

    ##### Statistical theory ############
    res_stat = StatisticalMat(geo, controls.freq, air.c0, air_m)
    res_stat.t60_sabine()
    res_stat.t60_eyring()
    # res_stat.t60_kutruff(gamma=0.4)
    res_stat.t60_araup()
    # res_stat.t60_fitzroy()
    # res_stat.t60_milsette()
    res_stat.plot_t60()

    ##### ray's initial direction ########
    rays_i_v = RayInitialDirections()
    # rays_i_v.single_ray([0.0, -1.0, 0.0])#([0.7236, -0.5257, 0.4472])
    # rays_i_v.isotropic_rays(controls.Nrays) # 15
    # mat = spio.loadmat('ra/vin_matlab.mat')
    # rays_i_v.vinit = mat['vin']
    rays_i_v.random_rays(controls.Nrays)
    # rays_i_v.single_ray(rays_i_v.vinit[41])
    log.info("The number of rays is {}.".format(rays_i_v.Nrays))
    print("The number of rays is {}.".format(rays_i_v.Nrays))


    ##### Setup receiver, reccross and reccrossdir ########
    receivers, reccross, reccrossdir = setup_receivers(cfgs['sim_cfg']['receivers'])
    #### Allocate some memory in python for geometrical ray tracing ########################
    # Estimate max reflection order
    N_max_ref = math.ceil(1.5 * air.c0 * controls.ht_length * \
        (geo.total_area / (4 * geo.volume)))
    # Allocate according to max reflection order
    rays = ray_initializer(rays_i_v, N_max_ref, controls.transition_order, reccross)

    ##### Setup sources - ray history goes inside source object ########
    sources = setup_sources(cfgs['sim_cfg']['sources'], rays, reccrossdir)

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
    # sou[0].plot_single_reflecrogram(band = 4, jrec = 2)
    # plt.show()
    # sou[0].plot_single_reflecrogram(band = 4, jrec = 1)
    sou[0].plot_decays()
    # sou[0].plot_edt()
    # sou[0].plot_t20()
    sou[1].plot_t30()
    # sou[0].plot_c80()
    # sou[0].plot_d50()
    # sou[0].plot_ts()
    # sou[0].plot_g()
    # sou[0].plot_lf()
    # sou[0].plot_lfc()
    # print(sources[0].rays[0].refpts_hist)
    # print(sources[0].rays[0].planes_hist)
    
    # geo.plot_raypath(sources[0].coord, sources[0].rays[0].refpts_hist,  # <-- sources[0].rays[0].refpts_hist
    #     receivers)
    # plt.show()
    # log.info(sources[0].reccrossdir[0].cos_dir)
    ############# Save trial #########################
    # flor = ra_cpp.Pet('flor', int(2))
    # flor.go_for_a_walk()
    # print(flor.get_name())
    # print(flor.get_hunger())
    # pick = ra_cpp.Pickleable("Pickable input")
    # pick.setExtra(15)
    import pickle
    path = '//home/eric/dev/ra/data/legacy/odeon_ex/'
    pkl_fname_res = 'odeon_ex_testpickle'        # simulation results name
    save_sim(controls=controls, air=air, rays_i = rays_i_v,
        geometry=geo, stats_theory=res_stat, sources=sources,
        receivers=receivers, s_reflecto_par=sou, stats_analysis=stats,
        path=path, fname=pkl_fname_res)
    # with open(path+pkl_fname_res+'.pkl', 'wb') as output:
    #     pickle.dump(geo, output, pickle.HIGHEST_PROTOCOL)
    #     pickle.dump(res_stat, output, pickle.HIGHEST_PROTOCOL)
    #     pickle.dump(sources, output, pickle.HIGHEST_PROTOCOL)
    #     pickle.dump(receivers, output, pickle.HIGHEST_PROTOCOL)
    #     pickle.dump(sou, output, pickle.HIGHEST_PROTOCOL)
    #     pickle.dump(stats, output, pickle.HIGHEST_PROTOCOL)
        # pickle.dump(flor, output, pickle.HIGHEST_PROTOCOL)
        # pickle.dump(pick, output, pickle.HIGHEST_PROTOCOL)
        # pickle.dump(sources, output, pickle.HIGHEST_PROTOCOL)
    
    # with open(path+pkl_fname_res+'.pkl', 'rb') as input:
    #     geo2 = pickle.load(input)
    #     res_stat = pickle.load(input)
    #     sources1 = pickle.load(input)
    #     # sou = pickle.load(input)
    #     # stats = pickle.load(input)
    #     # flor = pickle.load(input)
    #     # pick = pickle.load(input)

    # print("writting and loading done.")
    # geo2.plot_mat_room(normals = 'on')
    # print(sources1[0].rays[0].planes_hist)
    # print(sources1[0].rays[10].refpts_hist)
    # print(sources1[0].rays[1].recs[2].time_cross)
    # print(sources1[0].reccrossdir[0].time_dir)
    # geo.plot_raypath(sources1[0].coord, sources[0].rays[0].refpts_hist,  # <-- sources[0].rays[0].refpts_hist
    #     receivers)
    # print('Pickable methods are: {}, {} and {} ###.'.format(pick.value, pick.setExtra, pick.extra))
    # print(pick.extra())
    # flor.name = 'Florzinha'
    # flor.hunger = 3
    # flor.go_for_a_walk()
    # print('{} is {} hungry'.format(flor.name, flor.hunger))

cfg_dir = 'data/legacy/odeon_ex/'
cfgs = setup(cfg_dir)
run(cfgs)
# class Simulation():
#     def __init__(self,):
#         self.cfgs = {}
#         self.sources = []
#         self.receivers = []
#         self.geometry = {}

#     def set_configs(self, cfgs):
#         self.cfgs = cfgs['sim_cfg']
#         self.mat_cfg = cfgs['mat_cfg']
#         self.controls = AlgControls(self.cfgs['controls'])
#         self.air = AirProperties(self.cfgs['air'])
#         self.air_m = self.air.air_absorption(self.controls.freq)

#     def set_sources(self, srcs):
#         '''
#         Parameters:
#         ----------
#             srcs: list of Source's
#         '''
#         # self.rays_i_v = RayInitialDirections()
#         # self.rays_i_v.random_rays(self.controls.Nrays)
#         # log.info("The number of rays is {}.".format(self.rays_i_v.Nrays))

#         # c0 = self.air.c0
#         # htl = self.controls.ht_length
#         # area = self.geo.total_area
#         # volume = self.geo.volume
#         # N_max_ref = math.ceil(1.5 * c0 * htl * area / (4 * volume))
#         # rays = ray_initializer(
#         #     self.rays_i_v, N_max_ref, self.controls.transition_order,
#         #     self.reccross
#         # )
#         # self.sources = setup_sources(
#         #     self.cfgs['sources'], rays, self.reccrossdir
#         # )

#     def set_receivers(self, rcvrs):
#         '''
#         Parameters:
#         -----------
#             rcvrs: list of Receiver`s
#         '''
#         new_rcvrs = []
#         for r in rcvrs:
#             r.append({
#                 'position': r.coord,
#                 'orientation': r.orientation
#             })
#         self.receivers, self.reccross, self.reccrossdir = setup_receivers(
#             new_rcvrs
#         )

#         # self.receivers, self.reccross, self.reccrossdir = setup_receivers(
#         #     self.cfgs['receivers']
#         # )

#     def set_geometry(self, geom):
#         '''
#         Parameters:
#         -----------
#             geom: list of dicts with the following parameters: 'name',
#             'vertices', 'normal', alpha, s.
#         '''
#         # to be populated
#         # ...
#         pass

#         # cfgs = self.cfgs
#         # alpha_list = load_matdata_from_mat(cfgs['material'])
#         # alpha, s = get_alpha_s(
#         #     cfgs['geometry'], self.mat_cfg['material'], alpha_list
#         # )
#         # self.geo = GeometryMat(cfgs['geometry'], alpha, s)

#     def run(self, state):
#         '''
#         Parameters:
#         ----------
#         Return:
#         -------
#             dict with the following structure:
#             {
#                 'rays':,
#                 ''
#             }
#         '''
#         res_stat = StatisticalMat(
#             self.geo, self.controls.freq, self.air.c0, self.air_m
#         )
#         res_stat.t60_sabine()
#         res_stat.t60_eyring()
#         srcs, rcvrs = self.sources, self.receivers
#         srcs = ra_cpp._direct_sound(
#             srcs, rcvrs, self.controls.rec_radius_init,
#             self.geo.planes, self.air.c0, self.rays_i_v.vinit
#         )
#         ctls = self.controls
#         srcs = ra_cpp._raytracer_main(
#             ctls.ht_length, ctls.allow_scattering, ctls.transition_order,
#             ctls.rec_radius_init, ctls.alow_growth, ctls.rec_radius_final, srcs,
#             rcvrs, self.geo.planes, self.air.c0, self.rays_i_v.vinit
#         )
#         srcs = ra_cpp._intensity_main(ctls.rec_radius_init,
#             srcs, self.air.c0, self.air.m, res_stat.alphas_mtx)
#         sou = process_results(ctls.Dt, ctls.ht_length,
#             ctls.freq, srcs, rcvrs)
#         stats = SRStats(sou)

#     def stats(self,):
#         pass

#     def save(self,):
#         '''
#         Return:
#         ------
#             a dict with the state of the simulation.
#         '''
#         pass