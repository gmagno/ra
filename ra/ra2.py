
import codecs
import json
import time

import collada as co
import numpy as np
import toml
from tqdm import tqdm

from ra import rtrace as rt
from ra.source import (
    # CircleSource, ConicSource,
    IsotropicSource,
    # SingleRaySource
)

import ra_cpp

from ra.rayinidir import RayInitialDirections
# from ra.receivers import Receivers
from ra.receivers import setup_receivers
# from ra.sources import Sources
from ra.sources import setup_sources
from ra.controlsair import AlgControls
from ra.controlsair import AirProperties
from ra.room import Geometry, GeometryMat
from ra.absorption_database import load_matdata_from_mat
from ra.absorption_database import get_alpha_s
from ra.statistics import StatisticalMat




def main():

    ##### Test Alg controls ########
    controls = AlgControls('simulation.toml')
    # controls.setup_controls()
    # print(controls.Nrays)
    # print(controls.freq)
    # print(controls.Dt)
    # print(controls.alow_growth)

    ##### Test Alg controls ########
    air = AirProperties('simulation.toml')
    air_m = air.air_absorption(controls.freq)
    # print(air.rho0)
    # print(air.c0)
    # print(air.m)

    ##### Test materials #############
    alpha_list = load_matdata_from_mat('simulation.toml')  
    alpha, s = get_alpha_s('surface_mat_id.toml', alpha_list)
    
    ##### Test Geometry ###########
    geo = GeometryMat('simulation.toml', alpha, s)
    # geo.plot_mat_room(normals = 'on')
    # geo = Geometry('simulation.toml')
    #geo.plot_dae_room(normals = 'on')
    # for plane in geo.planes:
    #     print("Plane area: {}.".format(plane.area))
        # print("Plane absorption coefficient: {}.".format(plane.alpha))
        # print("Plane scaterring coefficient: {}.".format(plane.s))

        # print("Plane name: {}.".format(plane.name))
        # print("Plane normal: {}.".format(plane.normal))
        # print("Plane vertices: {}.".format(plane.vertices))
        # print("Plane v_x: {}. Plane v_y: {}.".format(plane.vert_x, plane.vert_y))
        # print("Plane centroid: {}.".format(plane.centroid))
    
    # print("The total area is {} m2.".format(geo.total_area))
    # print("The volume is {} m3.".format(geo.volume))
    
    
    

    ##### Test ray initiation ########
    rays_i_v = RayInitialDirections()
    rays_i_v.single_ray() 
    # rays_i_v.isotropic_rays(100)
    # rays_i_v.plot_arrows()
    # rays_i_v.plot_points()
    # print("Rays original directions: {}.".format(rays_i_v.vinit))
    
    ##### Test sources initiation ########
    sources = setup_sources('simulation.toml')
    # for js, s in enumerate(sources):
    #     print("Source {} coord: {}.".format(js, s.coord))
    #     print("Source {} orientation: {}.".format(js, s.orientation))
    #     print("Source {} power dB: {}.".format(js, s.power_dB))
    #     print("Source {} eq dB: {}.".format(js, s.eq_dB))
    #     print("Source {} power (linear): {}.".format(js, s.power_lin))

    
    ##### Test receiver initiation ########
    receivers = setup_receivers('simulation.toml')
    # for jrec, r in enumerate(receivers):
    #     print("Receiver {} coord: {}.".format(jrec, r.coord))
    #     print("Receiver {} coord: {}.".format(jrec, r.orientation))


    ##### Test statistical theory ############
    # res_stat = StatisticalMat(geo, controls.freq, air.c0, air_m)
    # res_stat.t60_sabine()
    # res_stat.t60_eyring()
    # res_stat.t60_kutruff(gamma=0.4)
    # res_stat.t60_araup()
    # res_stat.t60_fitzroy()
    # res_stat.t60_milsette()
    # res_stat.plot_t60()


    ############### Some ray tracing in python ##############
    # pet = ra_cpp.Pet('pluto', 5)
    # print(pet.get_name())
    # ra_cpp.ray_tracer(air)
    
    # for js, s in enumerate(sources):
    #     for jray, ray in enumerate(rays_i_v.vinit):
            

if __name__ == '__main__':
    main()
